from django.db import migrations


def clean_villages(apps, schema_editor):
    Village = apps.get_model('SamajApp', 'Village')
    Member = apps.get_model('SamajApp', 'Member')
    Family = apps.get_model('SamajApp', 'Family')

    def merge(from_id, into_id):
        """Re-point all Member/Family records from from_id → into_id, then delete from_id."""
        Member.objects.filter(current_address_village_id=from_id).update(current_address_village_id=into_id)
        Family.objects.filter(paitrik_address_village_id=from_id).update(paitrik_address_village_id=into_id)
        Village.objects.filter(id=from_id).delete()

    def rename(village_id, new_name):
        Village.objects.filter(id=village_id).update(village_name=new_name)

    def null_out(village_id):
        """Null the village FK on all linked records, then delete the village."""
        Member.objects.filter(current_address_village_id=village_id).update(current_address_village=None)
        Family.objects.filter(paitrik_address_village_id=village_id).update(paitrik_address_village=None)
        Village.objects.filter(id=village_id).delete()

    # ── Phase 1: Pure renames (garbled Unicode → correct ASCII) ──────────────
    rename(33,  'Atun')               # Āṭūṇ
    rename(179, 'Bhuvana')            # Bhuvānā
    rename(127, 'Khavasji Ka Rasta')  # KhavåSji Ka Rasta

    # ── Phase 2: Rename before merge (so the target name is right first) ─────
    rename(191, 'Bheru Ghati')        # Bhairudhati → Bheru Ghati
    rename(231, 'Sisarma Road')       # Sisarma Roar → Sisarma Road

    # ── Phase 3: Merges – full-address junk → clean canonical ────────────────
    # "Kanak Vihar Saiti, Chittaudgar/Chittorgarh, Rajasthan" → Kanak Vihar Saiti (75)
    merge(272, 75)
    merge(273, 75)

    # "Samtanagar, Senthi" → Samtanagar Saiti (86)
    merge(290, 86)

    # ── Phase 4: Merges – duplicate / misspelled → canonical ─────────────────
    merge(162, 300)   # Kāṅkaroli        → Kankroli        (Rajsamand)
    merge(278, 94)    # Baansi           → Bansi            (Chittorgarh)
    merge(163, 332)   # Rajasamand       → Rajsamand        (Rajsamand)
    merge(44,  322)   # Gyangadh (0 rec) → Gyangarh         (Bhilwara)
    merge(294, 320)   # Dipty            → Dipti             (Rajsamand)
    merge(314, 155)   # Ganesh Nagar Jawad → Ganesh Nagar   (Rajsamand)
    merge(315, 155)   # Ganesh Nagar Javad (0 rec) → Ganesh Nagar (Rajsamand)
    merge(281, 252)   # लोपडा            → Lopda            (Udaipur)
    merge(227, 231)   # Seesarama Roar   → Sisarma Road (231, renamed above)
    merge(321, 103)   # Kannoj           → Kanouj           (Chittorgarh)
    merge(327, 51)    # Khairabad        → Kherabad         (Bhilwara)
    merge(284, 191)   # Bhairu Ghati     → Bheru Ghati (191, renamed above)
    merge(293, 178)   # Shri N. Bhairavay Nagar → Bhairavay Nagar (Udaipur)
    merge(221, 73)    # Gandhinagar Chi  → Gandhinagar      (Chittorgarh)
    merge(159, 329)   # Koshivada (140 members) → Koshiwara (Rajsamand)

    # ── Phase 5: Safe delete – 0 records, wrong city ─────────────────────────
    Village.objects.filter(id=337).delete()  # "Kanak Vihar Saiti, Chittorgarh, Rajasthan" under Udaipur

    # ── Phase 6: Empty village name – null out 26 members, then delete ───────
    null_out(211)  # village_name="" under Udaipur


class Migration(migrations.Migration):

    dependencies = [
        ('SamajApp', '0032_correct_state_city_names'),
    ]

    operations = [
        migrations.RunPython(clean_villages, migrations.RunPython.noop),
    ]
