from django.db import models

class Slot(models.Model):
    slot_number = models.PositiveIntegerField(unique=True)

    # Front of card
    name = models.CharField(max_length=15)
    icon = models.URLField(max_length=500)
    front_bg_color = models.CharField(max_length=7, default="#016f4a")  # HEX color
    front_text_color = models.CharField(max_length=7, default="#ffffff")

    # Back of card
    message = models.TextField(max_length=100)
    link = models.URLField(blank=True, null=True)
    back_bg_color = models.CharField(max_length=7, default="#148a62")
    back_text_color = models.CharField(max_length=7, default="#ffffff")

    # Payment
    payment_proof = models.URLField(max_length=500)
    verified = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    # Email
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Slot {self.slot_number} - {'✔' if self.verified else '❌'} {self.name}"
