import os
import django
import random
from datetime import date, time
from faker import Faker

fake = Faker()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
django.setup()

from SamajApp.models import Family, Member, QualificationDetail, OccupationDetail, NewsEvent, Comment
from django.contrib.auth.models import User


gotras = ['Bharadwaj', 'Vashishtha', 'Kashyap']
locations = ['Udaipur', 'Ahmedabad', 'Jaipur']
degrees = ['B.Tech', 'B.Sc', 'MCA', 'MBA']
companies = ['TCS', 'Infosys', 'Wipro']
businesses = ['Paliwal Traders', 'Samaj Marble', 'Heritage Textiles']


def populate_users(n):
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = "password"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"Created user: {username}")
        else:
            print(f"User already exists: {username}")


# Create 3 families
families = []
def populate_families(n):
    global families
    for i in range(n):
        family_name = f"{fake.last_name()} Family"
        family_obj = Family(name=family_name)
        family_obj.save()
        families.append(family_obj)


# Create 10 members
members = []
def populate_members(n):
    global members
    for i in range(n):
        family = random.choice(families)
        user = random.choice(User.objects.all())
        member = Member.objects.create(
            family=family,
            user = user,
            father_name=f"{fake.first_name()} {fake.last_name()}",
            mother_name=f"{fake.first_name()} {fake.last_name()}",
            date_of_birth=date(1990 + i % 10, 1, 15),
            birth_place=random.choice(locations),
            birth_time=time(10 + i % 12, 30),
            gender=random.choice(['male', 'female']),
            marital_status=random.choice(['married', 'unmarried']),
            height=random.uniform(150, 180),
            phone_number=f"98765432{i:02}",
            whatsapp_number=f"98765432{i:02}",
            gotra=random.choice(gotras),
            current_address=random.choice(locations),
            qualification_type=random.choice(['school', 'undergraduate', 'graduate']),
            occupation_type=random.choice(['job', 'business'])
        )
        members.append(member)

        # Update one family head
        if not family.family_head:
            family.family_head = member
            family.save()

        # Qualification detail
        if member.qualification_type != 'school':
            QualificationDetail.objects.create(
                member=member,
                college_name='XYZ College',
                degree_name=random.choice(degrees)
            )
        else:
            QualificationDetail.objects.create(
                member=member,
                class_name='10th'
            )

        # Occupation detail
        if member.occupation_type == 'job':
            OccupationDetail.objects.create(
                member=member,
                company_name=random.choice(companies),
                company_location=random.choice(locations),
                job_description='Software Engineer'
            )
        else:
            OccupationDetail.objects.create(
                member=member,
                business_name=random.choice(businesses),
                business_location=random.choice(locations),
                business_description='Family owned business'
            )

# Create 5 news/events
def populate_news_and_events(n):
    for i in range(n):
        title = f"Sample Event {i + 1}"
        NewsEvent.objects.create(
            title=title,
            subtitle="This is a subtitle for event/news",
            image='news_events/sample.jpg',
            content="Detailed content about this event or news.",
            category=random.choice(['news', 'event']),
        )



# Create dummy comments
def populate_comments(n):
    posts = NewsEvent.objects.all()
    site_members = Member.objects.all()

    for _ in range(n):
        post = random.choice(posts)
        sender = random.choice(site_members)
        content = f"This is a comment by {sender.user} on {post.title}"
        comment = Comment.objects.create(
            post=post,
            sender=sender,
            content=content
        )

        # 50% chance of adding a reply
        if random.random() > 0.5:
            reply_sender = random.choice(site_members)
            Comment.objects.create(
                post=post,
                sender=reply_sender,
                content=f"Reply from {reply_sender.user} to {sender.user}'s comment",
                parent=comment
            )


if __name__ == "__main__":
    populate_users(9)
    populate_families(3)
    populate_members(10)
    populate_news_and_events(5)
    populate_comments(20)
print("Dummy data inserted successfully.")
