from django.db import models

class Slot(models.Model):
    slot_number = models.PositiveIntegerField(unique=True)

    # Front of card
    name = models.CharField(max_length=40)
    icon = models.URLField(max_length=500)
    front_bg_color = models.CharField(max_length=7, default="#016f4a")  # HEX color
    front_text_color = models.CharField(max_length=7, default="#ffffff")

    # Back of card
    message = models.TextField(max_length=150)
    link = models.URLField(blank=True, null=True)
    back_bg_color = models.CharField(max_length=7, default="#148a62")
    back_text_color = models.CharField(max_length=7, default="#ffffff")

    # Payment
    payment_proof = models.URLField(max_length=500)
    payment_reference_number = models.CharField(max_length=100, blank=True)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    verified = models.BooleanField(default=False)

    # Email
    email = models.EmailField(blank=True, null=True)

    # Admin Handling
    admin_remarks = models.TextField(max_length=500, blank=True, null=True)
    claimed_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Slot {self.slot_number} - {'✔' if self.verified else '❌'} {self.name}"
