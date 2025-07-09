from .models import Slot
from django.core.cache import cache

def get_all_slots_with_status():
    cache_key = "all_slots_with_status"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    total_slots = 20000
    all_claimed_slots = {slot.slot_number: slot for slot in Slot.objects.all()}

    all_slots = []

    for i in range(1, total_slots + 1):
        # Pricing logic
        if 1 <= i <= 20:
            price = 100
        elif i % 69 == 0:
            price = 1
        else:
            price = 69

        slot = all_claimed_slots.get(i)

        slot_data = {
            'slot_number': i,
            'claimed': bool(slot),
            'verified': slot.verified if slot else False,
            'price': f"{price:.2f}",

            # Common UI data (default to None if unclaimed)
            'name': slot.name if slot else None,
            'icon': slot.icon if slot else None,
            'front_bg_color': slot.front_bg_color if slot else None,
            'front_text_color': slot.front_text_color if slot else None,
            'message': slot.message if slot else None,
            'link': slot.link if slot else None,
            'back_bg_color': slot.back_bg_color if slot else None,
            'back_text_color': slot.back_text_color if slot else None,
        }

        all_slots.append(slot_data)

    cache.set(cache_key, all_slots, timeout=60)  # Cache for 1 minute
    return all_slots
