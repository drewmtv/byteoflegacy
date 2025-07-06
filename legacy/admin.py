from django.core.mail import send_mail
from django.contrib import admin
from .models import Slot

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'name', 'email', 'payment_amount', 'payment_proof', 'verified')
    actions = ['verify_and_notify']

    def verify_and_notify(self, request, queryset):
        updated = 0
        for slot in queryset:
            if not slot.verified:
                slot.verified = True
                slot.save()
                send_mail(
                    subject='Your Byte is Live!',
                    message=f"Hi {slot.name},\n\nYour Byte has been verified and is now live at slot #{slot.slot_number}!\n\nThank you!",
                    from_email=None,
                    recipient_list=[slot.email],
                    fail_silently=False,
                )
                updated += 1
        self.message_user(request, f"{updated} slots verified and notified.")
    verify_and_notify.short_description = "Verify selected slots and send email"