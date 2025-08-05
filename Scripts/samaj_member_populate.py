import os
import sys
import random

# 1) find the repo root: that's one level up from Extras/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 2) make sure Python can import your `paliwalsamaj` package
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
import django

django.setup()

from SamajApp.models import DisplayMember, DisplayMemberGroup
from django.core.files import File


role_data = {
	'adhyaksh': [
		('Shri Bheru Lal Paliwal', 'Kannauj', 'BHERU_LAL_JI_PALIWAL_kannauj.JPG', '9530164855')
	],
	'upadhyaksh': [
		('Shri Shobha Lal Paliwal', 'Kannauj', 'SHOBHA LAL JI PALIWAL.JPG', '7568930566')
	],
	'sachiv': [
		('Shri Pradeep Purohit', 'Chittorgarh', 'PRADEEP JI PUROHIT.JPG', '9413791302'),
	],
    'sanrakshak': [
        ('Shri D. S. Joshi', 'Chittorgarh', 'DS_JOSHI_SB.JPG'),
        ('Shri Ramchandra Purohit', 'Lopda', 'RAM CHANDAR JI PUROHIT.JPG'),
        ('Shri Premprakash Purohit', 'Shiro. ka Samta', 'PREM PRAKASH JI PUROHIT.JPG'),
        ('Shri Banshilal Paliwal', 'Kannauj', 'BANSHI LAL JI PUROHIT.JPG'),
        ('Shri Kanchanlal Paliwal', 'Bhootlavash', ''),
        ('Shri Amrutlal Purohit', 'Bherda', '')
    ],
    'mahila_adhyaksh': [
        ('Shrimati Sushma Purohit', 'Chittorgarh', 'SUSHMA JI PUROHIT.JPG')
    ],
    'koshadhyaksh': [
        ('Shri Premnarayan Paliwal', 'Bhootlavash', 'PREM NARAYAN JI PALIWAL.JPG')
    ],
    'saha_sachiv': [
        ('Shri Dinesh Kumar Purohit', 'Siyaliya', 'DINESH CHANDAR JI PUROHIT.JPG')
    ],
    'salahkaar': [
        ('Shri Azad Paliwal', 'Samta', 'azad_paliwal_salahkar.jpeg'),
        ('Shri Bherulal Purohit', 'Samta', 'BHERU LAL PALIWAL JI Samta.JPG'),
        ('Shri Chandrashekhar Purohit', 'Devgad', 'CHANDAR SHEKHAR JI PUROHIT.JPG'),
        ('Shri Narendra Paliwal', 'Tai', 'NARENDAR JI PALIWAL.JPG'),
        ('Shri Harish Purohit', 'Bherda', ''),
        ('Shri Kamlesh Purohit', 'Chittorgarh', ''),
        ('Shrimati Priyanka Paliwal', 'Chittorgarh', ''),
    ],
    'aayojan_samiti': [
        ('Shri Shankarlal Paliwal', 'Hoda', 'SHANKAR LAL JI PALIWAL.jpeg'),
        ('Shri Udaylal Paliwal', 'Kannauj', 'UDAY LAL JI PALIWAL.JPG'),
        ('Shri Himanshu Purohit', 'Samta', 'HIMANSHU JI SAMTA.JPG'),
        ('Shri Naresh Paliwal', 'Senti', ''),
    ],
    'karyakari_sadasya': [
        ('Shri Umesh Paliwal', 'Tai', 'UMESH JI PALIWAL.JPG'),
        ('Shri Mukesh Purohit', 'Aavlaheda', 'MUKESH JI PUROHIT.JPG'),
        ('Shri Piyush Purohit', 'Bherda', 'PIYUSH JI PUROHIT.JPG'),
        ('Shri Rameshchandra Purohit', 'Samta', 'RAMESH CHANDAR PUROHIT JI.JPG'),
        ('Shri Premraj Paliwal', 'Samta', ''),
        ('Shri Himanshu Purohit', 'Soniyana', ''),
        ('Shri Prakashchandra Purohit', 'Bengu', ''),
    ]
}

# Base path for your local static images
IMAGE_DIR = '../static/images/profile/'


def populate_members():
    groups = DisplayMemberGroup.objects.all()
    for role, members in role_data.items():
        for index, member in enumerate(members):
            if len(member) == 4:
                name, location, image_name, phone = member
            else:
                name, location, image_name = member
                phone = ''

            image_path = os.path.join(IMAGE_DIR, image_name) if image_name else None

            instance = DisplayMember(
                group = random.choice(groups),
                member_name=name,
                location=location,
                phone_number=phone,
                role=role,
                rank = index+1
            )

            if image_name and os.path.isfile(image_path):
                with open(image_path, 'rb') as img_file:
                    instance.member_image.save(f"samaj_display_members/{image_name}", File(img_file), save=False)

            instance.save()
            print(f"✅ Saved: {name} - Role: {role}")


def populate_groups():
    grp_list = ['Karyakarini Sadasya', 'Netritva Mandal', 'Sanchalan Samiti', 'Salah evam Aayojan Mandal']
    for idx, group in enumerate(grp_list):
        DisplayMemberGroup.objects.create(group_name=group, group_rank=idx+1)

if __name__ == "__main__":
    populate_groups()
    populate_members()
    print("Members Populated successfully.")
