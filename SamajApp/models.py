from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify


class Family(models.Model):
    class Meta:
        verbose_name_plural = 'Family'

    name = models.CharField(max_length=100)  # e.g., Sharma
    family_code = models.CharField(max_length=30, unique=True, editable=False)
    family_head = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_family')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.family_code:
            slug_name = slugify(self.name)
            suffix = str(uuid.uuid4())[:6].upper()
            self.family_code = f"{slug_name}-{suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} Family ({self.family_code})"



class Member(models.Model):
    class Meta:
        verbose_name_plural = 'Member'

    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]
    MARITAL_STATUS_CHOICES = [
        ('unmarried', _('Unmarried')),
        ('married', _('Married')),
    ]
    QUALIFICATION_CHOICES = [
        ('school', _('School')),
        ('undergraduate', _('Undergraduate')),
        ('graduate', _('Graduate')),
    ]
    OCCUPATION_CHOICES = [
        ('none', _('None')),
        ('job', _('Job')),
        ('business', _('Business')),
    ]
    GOTRA_CHOICES = [
        ('agastya', _('Agastya')),
        ('alambayana', _('Alambayana')),
        ('angirasa', _('Angirasa')),
        ('aankiras', _('Aankiras')),
        ('aarti', _('Aarti')),
        ('aashwalaayana', _('Aashwalaayana')),
        ('aatreya', _('Aatreya')),
        ('bhrigu', _('Bhrigu')),
        ('bhardwaja', _('Bhardwaja')),
        ('bhargava', _('Bhargava')),
        ('chandratreya', _('Chandratreya')),
        ('chyavana', _('Chyavana')),
        ('garga', _('Garga')),
        ('gautam', _('Gautam')),
        ('harita', _('Harita')),
        ('jamadagni', _('Jamadagni')),
        ('jambu', _('Jambu')),
        ('kaakshivan', _('Kaakshivan')),
        ('kanva', _('Kanva')),
        ('kapi', _('Kapi')),
        ('kashyapa', _('Kashyapa')),
        ('kaushika', _('Kaushika')),
        ('katyayana', _('Katyayana')),
        ('kaundinya', _('Kaundinya')),
        ('kutsa', _('Kutsa')),
        ('mandavya', _('Mandavya')),
        ('marichi', _('Marichi')),
        ('moudgalya', _('Moudgalya')),
        ('mrukandu', _('Mrukandu')),
        ('paingya', _('Paingya')),
        ('parashara', _('Parashara')),
        ('pulaha', _('Pulaha')),
        ('pulastya', _('Pulastya')),
        ('reva', _('Reva')),
        ('rishyashringa', _('Rishyashringa')),
        ('saandilya', _('Saandilya')),
        ('shaandilya', _('Shaandilya')),
        ('shakalya', _('Shakalya')),
        ('shandilya', _('Shandilya')),
        ('shatamarshana', _('Shatamarshana')),
        ('shaunak', _('Shaunak')),
        ('shukla', _('Shukla')),
        ('srivatsa', _('Srivatsa')),
        ('sutapa', _('Sutapa')),
        ('vadhoola', _('Vadhoola')),
        ('vasishta', _('Vasishta')),
        ('vatsa', _('Vatsa')),
        ('vishvamitra', _('Vishvamitra')),
        ('yajnavalkya', _('Yajnavalkya')),
    ]

    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, related_name='my_family')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    birth_place = models.CharField(max_length=100)
    birth_time = models.TimeField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Height in cm")
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES)
    current_address = models.TextField()
    current_address_city = models.TextField(max_length=100, null=True, blank=True)
    current_address_state = models.TextField(max_length=100, null=True, blank=True)
    current_address_pincode = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    qualification_type = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    occupation_type = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default='none')
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user}"


class QualificationDetail(models.Model):
    class Meta:
        verbose_name_plural = 'Qualification Details'
    DEGREE_CHOICES = [
        ("B.A.", _("B.A. (Bachelor of Arts)")),
        ("B.Sc.", _("B.Sc. (Bachelor of Science)")),
        ("B.Com.", _("B.Com. (Bachelor of Commerce)")),
        ("BBA", _("BBA (Bachelor of Business Administration)")),
        ("BCA", _("BCA (Bachelor of Computer Applications)")),
        ("B.Tech", _("B.Tech (Bachelor of Technology)")),
        ("BE", _("B.E. (Bachelor of Engineering)")),
        ("LLB", _("LLB (Bachelor of Laws)")),
        ("MBBS", _("MBBS (Bachelor of Medicine and Bachelor of Surgery)")),
        ("M.A.", _("M.A. (Master of Arts)")),
        ("M.Sc.", _("M.Sc. (Master of Science)")),
        ("M.Com.", _("M.Com. (Master of Commerce)")),
        ("MBA", _("MBA (Master of Business Administration)")),
        ("MCA", _("MCA (Master of Computer Applications)")),
        ("M.Tech", _("M.Tech (Master of Technology)")),
        ("ME", _("M.E. (Master of Engineering)")),
        ("LLM", _("LLM (Master of Laws)")),
        ("MD", _("MD (Doctor of Medicine)")),
        ("Diploma", _("Diploma")),
        ("ITI", _("ITI (Industrial Training Institute)")),
        ("Polytechnic", _("Polytechnic")),
        ("Certification", _("Certification Course")),
        ("PhD", _("Ph.D. (Doctor of Philosophy)")),
        ("D.Litt", _("D.Litt (Doctor of Literature)")),
        ("Other", _("Other")),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='qualification_detail')
    school_class = models.PositiveSmallIntegerField(blank=True, null=True)  # Only if School
    school_name = models.CharField(max_length=255, blank=True, null=True)
    college_name = models.CharField(max_length=100, blank=True, null=True)  # For UG/Graduate
    degree_name = models.CharField(choices=DEGREE_CHOICES, max_length=100, blank=True, null=True)  # For UG/Graduate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Qualification for {self.member}"


class OccupationDetail(models.Model):
    class Meta:
        verbose_name_plural = 'Occupation Details'

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='occupation_detail')
    # Job fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_location = models.CharField(max_length=255, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)

    # Business fields
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_location = models.CharField(max_length=255, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Occupation for {self.member.user}"


class NewsEvent(models.Model):
    class Meta:
        verbose_name_plural = 'News & Events'

    EVENT_TYPE_CHOICES = [
        ('news', 'News'),
        ('event', 'Event'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='news_events/')
    content = models.TextField()
    category = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(NewsEvent, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(NewsEvent, on_delete=models.CASCADE, related_name='comments')
    sender = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    def __str__(self):
        return f'Comment by {self.sender}'

    def is_reply(self):
        return self.parent is not None


class Newsletter(models.Model):
    class Meta:
        verbose_name_plural = 'Newsletter'

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class SamajMemberRoles(models.Model):
    class Meta:
        verbose_name_plural = 'Samaj Member Roles'

    ROLE_CHOICES = [
        ('sanrakshak', 'Sanrakshak'),
        ('mahila_adhyaksh', 'Mahila Adhyaksh'),
        ('koshadhyaksh', 'Koshadhyaksh'),
        ('saha_sachiv', 'Saha Sachiv'),
        ('salahkaar', 'Salahkaar'),
        ('aayojan_samiti', 'Aayojan Samiti'),
        ('karyakari_sadasya', 'Karyakari Sadasya'),
    ]
    member_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    member_image = models.FileField('samaj_role_members', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.member_name} - {self.role}"


class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"