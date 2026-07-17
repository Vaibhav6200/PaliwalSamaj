"""
Migration: Deduplicate State, City, and Village records.

Strategy:
- Normalize each name: strip whitespace, remove trailing pin codes
  (e.g. "Rajasthan 311001" → "Rajasthan")
- Group records by normalized name (case-insensitive)
- For each duplicate group, keep the oldest record (lowest pk) as canonical
- Re-point ALL FK references from duplicates to the canonical record:
    Member.current_address_state/city/village
    Family.paitrik_address_state/city/village
- Delete the duplicate records
"""

import re
from django.db import migrations


def normalize_name(name):
    """Strip whitespace and trailing 6-digit pin codes."""
    name = name.strip()
    # Remove trailing pin codes like "311001", " 313334"
    name = re.sub(r'\s+\d{6}$', '', name).strip()
    return name


def merge_city_into(city, canonical_city, apps):
    """Re-point all villages/members/families from city → canonical_city, then delete city."""
    Village = apps.get_model('SamajApp', 'Village')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    for village in Village.objects.filter(city=city):
        existing_village = Village.objects.filter(
            village_name__iexact=normalize_name(village.village_name),
            city=canonical_city
        ).first()
        if existing_village:
            Member.objects.filter(current_address_village=village).update(current_address_village=existing_village)
            Family.objects.filter(paitrik_address_village=village).update(paitrik_address_village=existing_village)
            village.delete()
        else:
            village.city = canonical_city
            village.save()

    Member.objects.filter(current_address_city=city).update(current_address_city=canonical_city)
    Family.objects.filter(paitrik_address_city=city).update(paitrik_address_city=canonical_city)
    city.delete()


def deduplicate_states(apps, schema_editor):
    State = apps.get_model('SamajApp', 'State')
    City = apps.get_model('SamajApp', 'City')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    # Group states by normalized lower-case name
    groups = {}
    for state in State.objects.all().order_by('id'):
        key = normalize_name(state.state_name).lower()
        groups.setdefault(key, []).append(state)

    for key, states in groups.items():
        if len(states) <= 1:
            continue

        canonical = states[0]  # oldest by pk
        duplicates = states[1:]

        print(f"[State] Merging {[s.state_name for s in duplicates]} → '{canonical.state_name}' (id={canonical.id})")

        for dup in duplicates:
            # Move each city from the duplicate state to the canonical state.
            # If a city with the same name already exists in the canonical state,
            # merge into it instead to avoid violating the unique_together constraint.
            for city in list(City.objects.filter(state=dup)):
                existing_city = City.objects.filter(
                    city_name__iexact=normalize_name(city.city_name),
                    state=canonical
                ).first()
                if existing_city:
                    print(f"  [City] '{city.city_name}' already in canonical state — merging into id={existing_city.id}")
                    merge_city_into(city, existing_city, apps)
                else:
                    city.state = canonical
                    city.save()

            Member.objects.filter(current_address_state=dup).update(current_address_state=canonical)
            Family.objects.filter(paitrik_address_state=dup).update(paitrik_address_state=canonical)
            dup.delete()


def deduplicate_cities(apps, schema_editor):
    City = apps.get_model('SamajApp', 'City')
    Village = apps.get_model('SamajApp', 'Village')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    # Group cities by (normalized lower-case city_name, state_id)
    groups = {}
    for city in City.objects.all().order_by('id'):
        key = (normalize_name(city.city_name).lower(), city.state_id)
        groups.setdefault(key, []).append(city)

    for key, cities in groups.items():
        if len(cities) <= 1:
            continue

        canonical = cities[0]
        duplicates = cities[1:]

        print(f"[City] Merging {[c.city_name for c in duplicates]} → '{canonical.city_name}' (id={canonical.id})")

        for dup in duplicates:
            Village.objects.filter(city=dup).update(city=canonical)
            Member.objects.filter(current_address_city=dup).update(current_address_city=canonical)
            Family.objects.filter(paitrik_address_city=dup).update(paitrik_address_city=canonical)
            dup.delete()


def deduplicate_villages(apps, schema_editor):
    Village = apps.get_model('SamajApp', 'Village')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    # Group villages by (normalized lower-case village_name, city_id)
    groups = {}
    for village in Village.objects.all().order_by('id'):
        key = (normalize_name(village.village_name).lower(), village.city_id)
        groups.setdefault(key, []).append(village)

    for key, villages in groups.items():
        if len(villages) <= 1:
            continue

        canonical = villages[0]
        duplicates = villages[1:]

        print(f"[Village] Merging {[v.village_name for v in duplicates]} → '{canonical.village_name}' (id={canonical.id})")

        for dup in duplicates:
            Member.objects.filter(current_address_village=dup).update(current_address_village=canonical)
            Family.objects.filter(paitrik_address_village=dup).update(paitrik_address_village=canonical)
            dup.delete()


def normalize_state_names(apps, schema_editor):
    """After deduplication, clean up remaining names (strip pin codes, extra spaces)."""
    State = apps.get_model('SamajApp', 'State')
    for state in State.objects.all():
        clean = normalize_name(state.state_name)
        if clean != state.state_name:
            print(f"[State] Renaming '{state.state_name}' → '{clean}'")
            state.state_name = clean
            state.save()


def normalize_city_names(apps, schema_editor):
    City = apps.get_model('SamajApp', 'City')
    for city in City.objects.all():
        clean = normalize_name(city.city_name)
        if clean != city.city_name:
            print(f"[City] Renaming '{city.city_name}' → '{clean}'")
            city.city_name = clean
            city.save()


def normalize_village_names(apps, schema_editor):
    Village = apps.get_model('SamajApp', 'Village')
    for village in Village.objects.all():
        clean = normalize_name(village.village_name)
        if clean != village.village_name:
            print(f"[Village] Renaming '{village.village_name}' → '{clean}'")
            village.village_name = clean
            village.save()


def run_all(apps, schema_editor):
    # Order matters: states first, then cities (depend on states), then villages
    deduplicate_states(apps, schema_editor)
    normalize_state_names(apps, schema_editor)
    deduplicate_cities(apps, schema_editor)
    normalize_city_names(apps, schema_editor)
    deduplicate_villages(apps, schema_editor)
    normalize_village_names(apps, schema_editor)


def reverse_noop(apps, schema_editor):
    # Deduplication is irreversible — data is gone
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('SamajApp', '0029_alter_family_family_code'),
    ]

    operations = [
        migrations.RunPython(run_all, reverse_noop),
    ]
