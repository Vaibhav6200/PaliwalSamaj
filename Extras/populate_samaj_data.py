import datetime
import pandas as pd
import os
import sys


# 1) find the repo root: that's one level up from Extras/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 2) make sure Python can import your `paliwalsamaj` package
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
import django

django.setup()


from SamajApp.models import Member, QualificationDetail, OccupationDetail, User, Family
from SamajApp.utils import generate_username
from django.db import transaction


def clean_string(value):
    return str(value).strip().lower() if pd.notna(value) else None


def parse_date(date_input):
    if not pd.notna(date_input):
        return None

    date_str = str(date_input).strip()

    # Handle full dates in DD-MM-YYYY or DD/MM/YYYY
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass

    # Handle full datetime in format YYYY-MM-DD HH:MM:SS
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
    except ValueError:
        pass

    # Handle date only in format YYYY-MM-DD
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass

    # Handle 4-digit year (e.g., 1994 or 1994.0)
    if date_str.isdigit() and len(date_str) == 4:
        return datetime.date(int(date_str), 1, 1)

    # Handle year with decimal (e.g., 1994.0)
    try:
        year = int(float(date_str))
        if 1000 <= year <= 9999:
            return datetime.date(year, 1, 1)
    except:
        pass

    # If nothing works
    raise ValueError(f"Unrecognized date format: '{date_input}'")


def parse_time(time_input):
    if not pd.notna(time_input):
        return None

    time_str = str(time_input).strip()

    # Handle cases like "13.0" ➝ "13:00"
    if time_str.replace('.', '', 1).isdigit():
        try:
            hour = int(float(time_str))
            if 0 <= hour < 24:
                return datetime.time(hour, 0)
        except:
            pass

    try:
        return datetime.datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Unrecognized time format: '{time_input}'")


def import_members_from_excel(filepath):
    print("📥 Starting import process from:", filepath)
    df = pd.read_excel(filepath)
    print(f"📊 Total records found: {len(df)}")

    family_map = {}
    head_candidates = {}
    allowed_degrees = ['ba', 'bsc', 'bcom', 'bba', 'bca', 'bpharma', 'btech', 'be', 'llb', 'ca', 'cs', 'mbbs', 'bped',
                       'bstc', 'stc', 'dllb', 'ma', 'msc', 'mcom', 'mba', 'mca', 'mtech', 'me', 'ms', 'med', 'mpharma',
                       'msw', 'llm', 'dlitt', 'phd', 'mch', 'md', 'pediatrician', 'bed', 'pgdca', 'iti', 'polytechnic',
                       'stenography', 'nursery', 'uneducated', 'primary', 'secondary', 'ssc', 'puc']

    try:
        with transaction.atomic():
            for i, (_, row) in enumerate(df.iterrows()):
                print()
                print(f"\n📌 Processing row {i + 1}...")

                family_id = row.get("family_id")
                paitrik_nivas = clean_string(row.get("paitrik_nivas"))
                paitrik_nivas_city = clean_string(row.get("paitrik_nivas_city"))
                paitrik_nivas_state = clean_string(row.get("paitrik_nivas_state"))
                paitrik_nivas_pincode = clean_string(row.get("paitrik_nivas_pincode"))
                full_name = clean_string(row.get("name"))
                qualification_type = clean_string(row.get("education_type"))
                occupation_type = clean_string(row.get("occupation_type"))
                occupation = clean_string(row.get("occupation"))
                email = clean_string(row.get("email"))
                father_name = clean_string(row.get("father_name"))
                dob = parse_date(row.get("dob"))
                birth_place = clean_string(row.get("birth_place"))
                birth_time = clean_string(row.get("birth_time"))
                gender = clean_string(row.get("gender"))
                marital_status = clean_string(row.get("marital_status"))
                height = int(row.get("height")) if pd.notna(row.get("height")) else None
                phone_number = str(row.get("phone_number")).strip() if pd.notna(row.get("phone_number")) else None
                whatsapp_no = str(row.get("whatsapp_no")).strip() if pd.notna(row.get("whatsapp_no")) else None
                gotra = clean_string(row.get("gotra"))
                current_address = clean_string(row.get("current_address"))
                current_address_city = clean_string(row.get("current_address_city"))
                current_address_state = clean_string(row.get("current_address_state"))
                current_address_pincode = clean_string(row.get("current_address_pincode"))
                relation_with_head = clean_string(row.get("relation_with_head"))
                school_class = clean_string(row.get("school_class"))
                raw_degree_string = clean_string(row.get("degree"))

                print(family_id, full_name, gotra, father_name, relation_with_head, phone_number, whatsapp_no, dob,
                      birth_place,
                      birth_time, gender, marital_status, height, email, current_address, current_address_city,
                      current_address_state, current_address_pincode, paitrik_nivas, paitrik_nivas_city,
                      paitrik_nivas_state,
                      paitrik_nivas_pincode, qualification_type, school_class, raw_degree_string, occupation_type, occupation)
                print()

                if pd.isna(family_id):
                    print("⚠️ Skipping row due to missing family_id")
                    continue

                # Create Family if not already created
                if family_id not in family_map:
                    family_name = f"Family {int(family_id)}"
                    family = Family.objects.create(
                        name=family_name,
                        paitrik_address=paitrik_nivas,
                        paitrik_address_city=paitrik_nivas_city,
                        paitrik_address_state=paitrik_nivas_state,
                        paitrik_address_pincode=paitrik_nivas_pincode,
                    )
                    family_map[family_id] = family
                    print(f"🏠 Created new family: {family.name} → {family.family_code}")
                else:
                    family = family_map[family_id]

                if qualification_type == 'school':
                    qualification_type = 'school'
                elif qualification_type == 'college':
                    qualification_type = 'undergraduate'
                elif qualification_type == 'graduate':
                    qualification_type = 'graduate'

                print(f"👤 Creating member: {full_name}")
                member = Member(
                    family=family,
                    user=User.objects.create(username=generate_username(full_name)),
                    full_name=full_name,
                    email=email,
                    father_name=father_name,
                    date_of_birth=dob,
                    birth_place=birth_place,
                    birth_time=birth_time,
                    gender=gender,
                    marital_status=marital_status,
                    height=height,
                    phone_number=phone_number,
                    whatsapp_number=whatsapp_no,
                    gotra=gotra,
                    current_address=current_address,
                    current_address_city=current_address_city,
                    current_address_state=current_address_state,
                    current_address_pincode=current_address_pincode,
                    qualification_type=qualification_type,
                )
                if occupation_type:
                    member.occupation_type = occupation_type
                member.save()
                print(f"✅ Member created: {member.full_name} (ID: {member.id})")

                # Check if this member is head of family
                if relation_with_head == "self":
                    head_candidates[family_id] = member
                    print("👑 Marked as head candidate for family")

                school_class_val = int(float(school_class)) if school_class else None
                if qualification_type == 'school':
                    QualificationDetail.objects.create(member=member, school_class=school_class_val)
                    print("🎓 Added school qualification")
                else:
                    if raw_degree_string:
                        for degree in raw_degree_string.split(","):
                            degree = degree.strip()
                            if not QualificationDetail.objects.filter(member=member, degree_name=degree).exists():
                                if degree in allowed_degrees:
                                    QualificationDetail.objects.create(member=member, degree_name=degree)
                                else:
                                    QualificationDetail.objects.create(member=member, degree_name='other', other_degree_text=degree)
                        print(f"🎓 Added degree qualification")

                if occupation_type == 'job':
                    OccupationDetail.objects.create(member=member, job_description=occupation)
                    print("💼 Job details added")
                elif occupation_type == 'business':
                    OccupationDetail.objects.create(member=member, business_description=occupation)
                    print("🏢 Business details added")

            # Assign family head now that all members are created
            print("\n🧾 Finalizing head assignments...")
            for fid, head_member in head_candidates.items():
                family = family_map.get(fid)
                if family:
                    family.family_head = head_member
                    family.save()
                    print(f"✔️ Family head assigned: {head_member.full_name} → {family.family_code}")


    except Exception as e:
        print("An error occured during import")
        print(f"{e}")
        raise

if __name__ == "__main__":
    data_sheet_path = './paliwal_samaj_data_unicode.xlsx'

    print("🚀 Starting member import script...")
    if not os.path.exists(data_sheet_path):
        print(f"❌ File not found: {data_sheet_path}")
    else:
        try:
            print(f"📂 Found file: {data_sheet_path}")
            print("📡 Importing members from Excel...\n")
            import_members_from_excel(filepath=data_sheet_path)
            print("\n✅ All members imported successfully!")
        except Exception as e:
            print("🔥 An error occurred during import:")
            print(f"🛑 {e}")
