from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Slot
from .forms import SlotForm
from .utils import upload_to_supabase_media, upload_to_supabase_confidential
from .helpers import get_all_slots_with_status  # assuming you have this utility
from .validators import validate_image_file

# Homepage – shows the mosaic wall
def index(request):
    all_slots = get_all_slots_with_status()
    return render(request, 'legacy/index.html', {'slots': all_slots})

# About page
def about(request):
    return render(request, 'legacy/about.html')

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

            return redirect('legacy:success')
    else:
        form = SlotForm(initial={'slot_number': slot} if slot else {})

    all_slots = get_all_slots_with_status()

    return render(request, 'legacy/claim_byte.html', {
        'form': form,
        'slot': slot,
        'all_slots': all_slots,
    })

# Success confirmation page
def claim_success(request):
    return render(request, "legacy/claim_success.html")