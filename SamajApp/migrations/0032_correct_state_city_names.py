"""
Migration: Correct state and city names based on manual review.

States:
- Rename: rajasthan→Rajasthan, gujarat→Gujarat, maharashtra→Maharashtra,
          karnataka→Karnataka, madhyapradesh→Madhya Pradesh, uttarakhanda→Uttarakhand
- Merge:  gujrart+gujrat → Gujarat, mp+rajsthan → canonical, mapra → Madhya Pradesh,
          chittaudgarh+udaipur-state → Rajasthan
- Delete: augh(9), empty(18), --select--(19)

Cities:
- Merge:  bhilwada+bhilwaracity → Bhilwara, chittaurgarh+chittaurgadh → Chittorgarh,
          mandsore → Mandsaur, rajasamand+rajsmand → Rajsamand,
          udaipur(35) → Udaipur(3), baroda(36) → Baroda(37),
          neemch(mapra) → neemch(MP)
- Rename: baroda→Baroda, baigaluru→Bengaluru, kāṅkaroli→Kankroli, kachch→Kutch,
          pratapgadh→Pratapgarh, neemch(10+18)→Neemuch
- Delete: empty(46), augh(26)
"""

from django.db import migrations


# ── Helpers ───────────────────────────────────────────────────────────────────

def move_villages(source_city, target_city, apps):
    """Move villages from source_city to target_city, merging conflicts."""
    Village = apps.get_model('SamajApp', 'Village')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    for village in list(Village.objects.filter(city=source_city)):
        existing = Village.objects.filter(
            village_name__iexact=village.village_name,
            city=target_city
        ).first()
        if existing:
            Member.objects.filter(current_address_village=village).update(current_address_village=existing)
            Family.objects.filter(paitrik_address_village=village).update(paitrik_address_village=existing)
            village.delete()
        else:
            village.city = target_city
            village.save()


def merge_city(source_id, target_id, apps):
    """Merge source city into target city, re-pointing all FKs."""
    City = apps.get_model('SamajApp', 'City')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    source = City.objects.filter(id=source_id).first()
    target = City.objects.filter(id=target_id).first()
    if not source or not target:
        print(f"  [skip] merge_city({source_id}→{target_id}): one or both not found")
        return

    print(f"  [City] Merging '{source.city_name}'({source_id}) → '{target.city_name}'({target_id})")
    move_villages(source, target, apps)
    Member.objects.filter(current_address_city=source).update(current_address_city=target)
    Family.objects.filter(paitrik_address_city=source).update(paitrik_address_city=target)
    source.delete()


def move_cities(source_state, target_state, apps):
    """Move cities from source_state to target_state, merging conflicts."""
    City = apps.get_model('SamajApp', 'City')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    for city in list(City.objects.filter(state=source_state)):
        existing = City.objects.filter(
            city_name__iexact=city.city_name,
            state=target_state
        ).first()
        if existing:
            move_villages(city, existing, apps)
            Member.objects.filter(current_address_city=city).update(current_address_city=existing)
            Family.objects.filter(paitrik_address_city=city).update(paitrik_address_city=existing)
            city.delete()
        else:
            city.state = target_state
            city.save()


def merge_state(source_id, target_id, apps):
    """Merge source state into target state, re-pointing all FKs."""
    State = apps.get_model('SamajApp', 'State')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    source = State.objects.filter(id=source_id).first()
    target = State.objects.filter(id=target_id).first()
    if not source or not target:
        print(f"  [skip] merge_state({source_id}→{target_id}): one or both not found")
        return

    print(f"[State] Merging '{source.state_name}'({source_id}) → '{target.state_name}'({target_id})")
    move_cities(source, target, apps)
    Member.objects.filter(current_address_state=source).update(current_address_state=target)
    Family.objects.filter(paitrik_address_state=source).update(paitrik_address_state=target)
    source.delete()


# ── Main ──────────────────────────────────────────────────────────────────────

def apply_corrections(apps, schema_editor):
    State = apps.get_model('SamajApp', 'State')
    City = apps.get_model('SamajApp', 'City')

    # ── PHASE 1: Merge duplicate/wrong cities ─────────────────────────────────
    # Must happen before states are renamed/merged so FKs are still valid.
    print("\n=== Phase 1: City merges ===")
    merge_city(1,  40, apps)   # bhilwada       → Bhilwara
    merge_city(47, 40, apps)   # bhilwaracity   → Bhilwara
    merge_city(45,  8, apps)   # chittaurgarh   → Chittorgarh
    merge_city(51,  8, apps)   # chittaurgadh   → Chittorgarh
    merge_city(19, 13, apps)   # mandsore       → Mandsaur
    merge_city(6,  33, apps)   # rajasamand     → Rajsamand
    merge_city(49, 33, apps)   # rajsmand       → Rajsamand
    merge_city(35,  3, apps)   # udaipur(fake)  → Udaipur(Rajasthan)
    merge_city(36, 37, apps)   # baroda(gujrart)→ baroda(gujrat)
    merge_city(9,  18, apps)   # neemch(mapra)  → neemch(Madhya Pradesh)

    # ── PHASE 2: Delete junk cities (0 records) ───────────────────────────────
    print("\n=== Phase 2: Delete junk cities ===")
    City.objects.filter(id=26).delete()   # augh city
    City.objects.filter(id=46).delete()   # empty city

    # ── PHASE 3: Re-assign fake states → real states, then delete ─────────────
    print("\n=== Phase 3: Fix fake states ===")
    merge_state(23,  1, apps)   # chittaudgarh → Rajasthan (id=1)
    merge_state(13,  1, apps)   # udaipur-state → Rajasthan
    merge_state(2,   4, apps)   # mapra         → Madhya Pradesh (id=4)
    merge_state(19,  1, apps)   # --select--    → Rajasthan (safe default)

    # Delete zero-record junk states
    State.objects.filter(id=9).delete()    # augh
    State.objects.filter(id=18).delete()   # empty string

    # ── PHASE 4: Rename states ────────────────────────────────────────────────
    print("\n=== Phase 4: Rename states ===")
    STATE_RENAMES = {
        1: 'Rajasthan',
        6: 'Gujarat',
        7: 'Maharashtra',
        8: 'Karnataka',
        4: 'Madhya Pradesh',
        5: 'Uttarakhand',
        3: 'Haryana',
    }
    for state_id, new_name in STATE_RENAMES.items():
        old = State.objects.filter(id=state_id).first()
        if old:
            print(f"  [State] '{old.state_name}' → '{new_name}'")
            State.objects.filter(id=state_id).update(state_name=new_name)

    # ── PHASE 5: Merge remaining duplicate states ─────────────────────────────
    print("\n=== Phase 5: Merge duplicate states ===")
    merge_state(14,  6, apps)   # gujrart  → Gujarat
    merge_state(15,  6, apps)   # gujrat   → Gujarat
    merge_state(21,  4, apps)   # mp       → Madhya Pradesh
    merge_state(22,  1, apps)   # rajsthan → Rajasthan

    # ── PHASE 6: Rename cities ────────────────────────────────────────────────
    print("\n=== Phase 6: Rename cities ===")
    CITY_RENAMES = {
        37: 'Baroda',
        22: 'Bengaluru',
        12: 'Kankroli',
        16: 'Kutch',
         5: 'Pratapgarh',
        10: 'Neemuch',   # under Rajasthan
        18: 'Neemuch',   # under Madhya Pradesh
    }
    for city_id, new_name in CITY_RENAMES.items():
        old = City.objects.filter(id=city_id).first()
        if old:
            print(f"  [City] '{old.city_name}' → '{new_name}'")
            City.objects.filter(id=city_id).update(city_name=new_name)

    print("\n=== Done ===")


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('SamajApp', '0031_alter_state_name_unique'),
    ]

    operations = [
        migrations.RunPython(apply_corrections, reverse_noop),
    ]
