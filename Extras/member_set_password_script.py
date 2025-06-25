import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
import django
from openpyxl import Workbook

django.setup()


from SamajApp.models import Member
from SamajApp.utils import generate_random_password


def set_member_passwords():
    wb = Workbook()
    ws = wb.active
    ws.title = "Passwords"
    ws.append(["Member ID", "Username", "Phone Number", "New Password"])

    for idx, member in enumerate(Member.objects.all()):
        password = generate_random_password()
        member.user.set_password(password)
        member.user.save()
        print(f"{idx + 1}:  setting password for : {member.full_name} - {password}")
        ws.append([member.id, member.user.username, member.phone_number, password])

    # Save to Excel file
    wb.save("generated_passwords.xlsx")
    print("Passwords written to generated_passwords.xlsx")

if __name__ == "__main__":
    set_member_passwords()
