from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.conf import settings
from urllib.parse import unquote # from django.utils.http import urlunquote REPLACED //

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Slot
from .forms import SlotForm
from .utils import upload_to_supabase_media, upload_to_supabase_confidential
from .helpers import get_all_slots_with_status, get_price_by_slot_number, is_claimed, is_verified
from .validators import validate_image_file

import os
import environ

env = environ.Env()

# Homepage – shows the mosaic wall
def index(request):
    all_slots = get_all_slots_with_status()
    return render(request, 'legacy/index.html', {'slots': all_slots})

# About page
def about(request):
    return render(request, 'legacy/about.html')

def card_info_link(request, slot, name=None):
    filtered_slot = Slot.objects.filter(slot_number=slot).values(
        'slot_number', 'name', 'icon', 'front_bg_color', 'front_text_color',
        'message', 'link', 'back_bg_color', 'back_text_color'
    ).first()

    # If slot doesn't exist, redirect to claim
    if filtered_slot is None:
        return redirect("legacy:claim", slot=slot)

    # If 'name' is not provided, redirect to full URL including name
    if name is None:
        return redirect("legacy:card-info-link", slot=slot, name=filtered_slot['name'])

    # If slot exists and name is provided, render the page
    if settings.DEBUG:
        absolute_icon = request.build_absolute_uri(filtered_slot['icon'])
    else:
        absolute_icon = filtered_slot['icon']

    return render(request, "legacy/card_info.html", {
        "slot": filtered_slot,
        "absolute_icon": absolute_icon,
    })

# New chunk view for AJAX requests
def slot_chunk_view(request):
    MAX_LIMIT = 300
    try:
        offset = int(request.GET.get('offset', 0))
        limit = min(int(request.GET.get('limit', 20)), MAX_LIMIT)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid offset or limit'}, status=400)

    try:
        all_slots = get_all_slots_with_status() or []
        sliced = all_slots[offset:offset + limit]

        slot_data = [
            {
                'slot_number': slot['slot_number'],
                'claimed': slot['claimed'],
                'price': slot['price'],
                'verified': slot['verified'],
                'name': slot['name'],
                'icon': slot['icon'],
                'front_bg_color': slot['front_bg_color'],
                'front_text_color': slot['front_text_color'],
                'message': slot['message'],
                'link': slot['link'],
                'back_bg_color': slot['back_bg_color'],
                'back_text_color': slot['back_text_color'],
            }
            for slot in sliced
        ]

        return JsonResponse({'slots': slot_data})

    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

# Claim a byte view
def claim_byte(request, slot=None):
    if request.method == 'POST':
        form = SlotForm(request.POST, request.FILES)
        slot_number = int(request.POST.get('slot_number', 0))

        if Slot.objects.filter(slot_number=slot_number).exists():
            messages.error(request, f"Slot {slot_number} is already taken or pending.")
        elif form.is_valid():
            # ✅ Now it's safe to grab files
            icon_file = request.FILES.get('icon')
            proof_file = request.FILES.get('payment_proof')

            try:
                validate_image_file(icon_file, max_size_mb=10)
                validate_image_file(proof_file, max_size_mb=10)
                
                icon_url = upload_to_supabase_media(icon_file, f"icons/{slot_number}_{icon_file.name}")
                proof_url = upload_to_supabase_confidential(proof_file, f"payments/{slot_number}_{proof_file.name}")

            except Exception as e:
                messages.error(request, f"Upload failed: {str(e)}")
                return render(request, 'legacy/claim_byte.html', {
                    'form': form,
                    'slot': slot,
                    'all_slots': get_all_slots_with_status(),
                    'messages': messages,
                })

            # ✅ Save but inject Supabase URLs instead of files
            slot = form.save(commit=False)
            slot.icon = icon_url  # now it's okay to overwrite
            slot.payment_proof = proof_url
            slot.verified = False
            slot.save()

            # Email logic
            send_mail(
                subject='Your Byte is Pending Verification',
                message=f"Hi {slot.name},\n\nThanks for claiming slot #{slot.slot_number}! We'll verify your payment and publish it soon.",
                from_email=None,
                recipient_list=[slot.email],
                fail_silently=False,
            )

            # Invalidate the cached slot list
            cache.delete("all_slots_with_status")

            return redirect('legacy:success')
    else:
        if is_claimed(slot):
            if is_verified(slot):
                return redirect('legacy:card-info-link', slot=slot)
            else:
                return render(request, 'legacy/claim_byte.html', {
                'form': form,
                'slot': slot,
                'all_slots': all_slots,
            })
        form = SlotForm(initial={'slot_number': slot, 'payment_amount': get_price_by_slot_number(slot)} if slot else {})

    all_slots = get_all_slots_with_status()

    return render(request, 'legacy/claim_byte.html', {
        'form': form,
        'slot': slot,
        'all_slots': all_slots,
    })

# Success confirmation page
def claim_success(request):
    return render(request, "legacy/claim_success.html")

# Mobile Admin Login View
def mobile_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('legacy:mobile-admin-dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid credentials.")  # Show error message if credentials are wrong
    
    return render(request, 'legacy/mobile-admin/mobile-admin-login.html')  # Render login page if GET request

# Mobile Logout View
def mobile_admin_logout(request):
    logout(request)
    return redirect('legacy:mobile-admin-login')  # Redirect to login page

# Mobile Admin Dashboard View (Protected by Login)
@login_required(login_url='legacy:mobile-admin-login')  # Redirect to login if not logged in
def mobile_admin_dashboard(request):
    # Your logic for rendering the admin dashboard
    return render(request, 'legacy/mobile-admin/mobile-admin-dashboard.html')

@csrf_exempt
def update_admin_remarks(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        admin_remarks = request.POST.get('admin_remarks')
        reference_number = request.POST.get('reference_number', '')  # New field for reference number

        # Get the Slot object
        slot = Slot.objects.get(id=slot_id)

        # Update the admin remarks and reference number
        slot.admin_remarks = admin_remarks
        slot.payment_reference_number = reference_number
        slot.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'})

def get_updated_slots(request):
    # Retrieve all slots or filter them based on your logic
    slots = Slot.objects.all().order_by("-claimed_date").values(
        'id',  # Add ID to identify each slot in the front end
        'slot_number', 
        'name', 
        'payment_amount', 
        'verified', 
        'payment_proof',  
        'claimed_date', 
        'admin_remarks', 
        'payment_reference_number'  # Add the reference number to the response
    )

    # Return the slot data as JSON
    return JsonResponse({'slots': list(slots)})

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='legacy:mobile-admin-login')
def fetch_proof_image(request, image_path):
    """
    Securely fetch a private Supabase image for admins only.
    """
    SUPABASE_URL = os.environ.get('Supabase_URL')
    SUPABASE_KEY = os.environ.get('Supabase_SERVICE_KEY')
    SUPABASE_BUCKET = os.environ.get('Supabase_STORAGE_BUCKET_CONFIDENTIAL')

    # Decode URL encoding if passed in path
    image_path = unquote(image_path)

    # Prevent path traversal
    if '..' in image_path or image_path.startswith('/'):
        raise Http404("Invalid path.")

    file_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{image_path}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        return HttpResponse(response.content, content_type=content_type)
    else:
        raise Http404("Image not found or access denied.")

def page_not_found(request, exception):
    # Redirect to the homepage or any other page
    return HttpResponseRedirect('/')