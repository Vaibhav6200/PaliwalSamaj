import datetime
import pandas as pd
from SamajApp.models import Member, QualificationDetail, OccupationDetail, User, Family


def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    except:
        return None


def parse_time(time_str):
    try:
        return datetime.datetime.strptime(time_str.strip(), "%H:%M").time()
    except:
        return None


def import_members_from_excel(filepath, default_user_id):
    df = pd.read_excel(filepath)

    for _, row in df.iterrows():
        try:
            family_id = row.get("Family Id")
            family = Family.objects.filter(id=family_id).first() if family_id else None

            member = Member.objects.create(
                user=User.objects.get(id=default_user_id),
                family=family,
                first_name=row.get("Name", "").split()[0],
                last_name=' '.join(row.get("Name", "").split()[1:]) or None,
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
            print(f"Imported: {member.first_name} {member.last_name}")
        except Exception as e:
            print(f"Failed to import row: {row.get('Name')} due to error: {e}")





if __name__ == "__main__":
    pass