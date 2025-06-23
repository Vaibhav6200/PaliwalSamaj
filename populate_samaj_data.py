import datetime
import pandas as pd
from SamajApp.models import Member, QualificationDetail, OccupationDetail, User, Family


def clean_string(value):
    return str(value).strip() if pd.notna(value) else None


def parse_date(date_input):
    if not date_input or str(date_input).lower() == 'nan':
        return None  # or return a default date if needed

    date_str = str(date_input).strip()

    # Handle full dates in DD-MM-YYYY or DD/MM/YYYY
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass

    # Handle 4-digit year (e.g., 1994 or 1994.0)
    if date_str.isdigit() and len(date_str) == 4:
        return datetime.date(int(date_str), 1, 1)

    # If it's like 1994.0, cast to int safely
    try:
        year = int(float(date_str))
        if 1000 <= year <= 9999:
            return datetime.date(year, 1, 1)
    except:
        pass

    # If nothing works
    raise ValueError(f"Unrecognized date format: '{date_input}'")


def parse_time(time_input):
    if not time_input or str(time_input).lower() == 'nan':
        return None  # or return datetime.time(0, 0) as a default

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


def import_members_from_excel(filepath, default_user_id):
    df = pd.read_excel(filepath)
    family_map = {}  # Map to track created families

    for _, row in df.iterrows():
        try:
            family_id = row.get("family_id")

            # Avoid duplicate family creation
            if family_id not in family_map:
                family_name = f"Family {int(family_id)}"
                family = Family.objects.create(name=family_name)
                family_map[family_id] = family
            else:
                family = family_map[family_id]

            full_name = clean_string(row.get("name"))
            gotra = clean_string(row.get("gotra"))
            father_name = clean_string(row.get("father_name"))

            dob = row.get("dob")
            birth_place = row.get("birth_place")
            birth_time = row.get("birth_time")
            gender = row.get("gender")
            marital_status = row.get("marital_status")
            height = row.get("height")
            phone_number = row.get("phone_number")
            whatsApp_no = row.get("whatsApp_no")
            current_address = row.get("current_address")
            current_address_city = row.get("current_address_city")
            current_address_state = row.get("current_address_state")
            current_address_pincode = row.get("current_address_pincode")

            paitrik_nivas = row.get("paitrik_nivas")
            paitrik_nivas_city = row.get("paitrik_nivas_city")
            paitrik_nivas_state = row.get("paitrik_nivas_state")
            paitrik_nivas_pincode = row.get("paitrik_nivas_pincode")

            family_head = row.get("family_head")
            relation_with_head = row.get("relation_with_head")
            email = row.get("email")
            education_type = row.get("education_type")
            school_class = row.get("school_class")
            degree = row.get("degree")
            occupation_type = row.get("occupation_type")
            occupation = row.get("occupation")
            location = row.get("location")
            company_name = row.get("company_name")
            job_description = row.get("job_description")
            business_description = row.get("business_description")



            if pd.isna(row.get("Company Name")):
                print("No Value Found")
            else:
                print(row.get("Company Name"))



            family_id = row.get("Family Id")
            family = Family.objects.filter(id=family_id).first() if family_id else None

            member = Member.objects.create(
                user=User.objects.get(id=default_user_id),
                family=family,
                full_name=row.get("Name", ""),
                father_name=row.get("Father Name"),
                date_of_birth=parse_date(row.get("Date of Birth (dd/mm/yyyy)")),
                birth_place=row.get("Birth Place"),
                birth_time=parse_time(row.get("Birth Time (24 Hr Format)")),
                gender=row.get("Gender \n(Male/Female)").lower(),
                marital_status=row.get("Marital Status \n(Unmarried / Married)").lower(),
                height=row.get("Height (cm)"),
                phone_number=str(row.get("Phone Number")),
                whatsapp_number=str(row.get("WhatsApp No")),
                gotra=row.get("Gotra").lower(),
                current_address=row.get("Current Address"),
                current_address_city=row.get("Current Address\n (City)"),
                current_address_state=row.get("Current Address\n (State)"),
                current_address_pincode=str(row.get("Current Address\n (Pincode)")),
                qualification_type=row.get("Education Type (School/College/Graduated)").lower(),
                occupation_type=row.get("Occupation (Student/Job/Business/Retired/Housewife)").lower() if row.get("Occupation (Student/Job/Business/Retired/Housewife)") else 'none',
            )

            if member.qualification_type == 'school':
                QualificationDetail.objects.create(
                    member=member,
                    school_class=int(row.get("Class \n(if School)") or 0),
                    school_name=row.get("Current Address\n (City)")
                )
            else:
                QualificationDetail.objects.create(
                    member=member,
                    college_name=row.get("Current Address\n (City)"),
                    degree_name=row.get("Degree (if College or Graduated)")
                )

            if member.occupation_type == 'job':
                OccupationDetail.objects.create(
                    member=member,
                    company_name=row.get("Company Name"),
                    company_location=row.get("Location"),
                    job_description=row.get("Job Description \n(if Job)")
                )
            elif member.occupation_type == 'business':
                OccupationDetail.objects.create(
                    member=member,
                    business_name=row.get("Company Name"),
                    business_location=row.get("Location"),
                    business_description=row.get("Business Description (if Business)")
                )
            print(f"Imported: {member.full_name}")
        except Exception as e:
            print(f"Failed to import row: {row.get('Name')} due to error: {e}")





if __name__ == "__main__":
    pass