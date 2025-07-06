from .models import Slot

def get_all_slots_with_status():
    total_slots = 20000
    all_claimed_slots = {slot.slot_number: slot for slot in Slot.objects.all()}

    all_slots = []
    for i in range(1, total_slots + 1):
        # Pricing logic
        if 1 <= i <= 10:  # FIXED: incorrect condition
            price = 100
        elif i % 69 == 0:  # FIXED: used %% instead of %
            price = 1
        else:
            price = 69  # DEFAULT price if not special range

        slot = all_claimed_slots.get(i)
        all_slots.append({
            'slot_number': i,
            'claimed': bool(slot),  # True if a Slot exists
            'verified': slot.verified if slot else False,
            'data': slot,  # The Slot instance or None
            'price': f"₱{price}",
        })

    return all_slots