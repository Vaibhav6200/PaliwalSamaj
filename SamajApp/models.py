from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
import datetime
from urllib.parse import urlparse, parse_qs
from django_ckeditor_5.fields import CKEditor5Field


class Family(models.Model):
    class Meta:
        verbose_name_plural = 'Family'

    name = models.CharField(max_length=100)  # e.g., Sharma
    family_code = models.CharField(max_length=30, unique=True, editable=False)
    family_head = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_family')
    paitrik_address = models.TextField(null=True, blank=True)
    paitrik_address_village = models.TextField(max_length=100, null=True, blank=True)
    paitrik_address_city = models.TextField(max_length=100, null=True, blank=True)
    paitrik_address_state = models.TextField(max_length=100, null=True, blank=True)
    paitrik_address_pincode = models.CharField(max_length=10, null=True, blank=True)
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
        ('aastik', _('Aastik')),        # Sheet
        ('aatreya', _('Aatreya')),
        ('baneda', _('Baneda')),        # Sheet
        ('bhrigu', _('Bhrigu')),
        ('bharadwaja', _('Bharadwaja')),        # Sheet
        ('bhargava', _('Bhargava')),
        ('chandratreya', _('Chandratreya')),
        ('chyavana', _('Chyavana')),
        ('dave', _('Dave')),        # Sheet
        ('garga', _('Garga')),
        ('gautam', _('Gautam')),
        ('harita', _('Harita')),
        ('jamadagni', _('Jamadagni')),
        ('jambu', _('Jambu')),
        ('joshi', _('Joshi')),        # Sheet
        ('kaakshivan', _('Kaakshivan')),
        ('kanva', _('Kanva')),
        ('kapi', _('Kapi')),
        ('kashyapa', _('Kashyapa')),        # Sheet
        ('kaushika', _('Kaushika')),
        ('kavachh', _('Kavachh')),        # Sheet
        ('katyayana', _('Katyayana')),
        ('kaundinya', _('Kaundinya')),
        ('kavachhas', _('Kavachhas')),        # Sheet
        ('kauts', _('Kauts')),        # Sheet
        ('kotsas', _('Kotsas')),        # Sheet
        ('kutsa', _('Kutsa')),
        ('mandavya', _('Mandavya')),
        ('marichi', _('Marichi')),
        ('moudgalya', _('Moudgalya')),
        ('mrukandu', _('Mrukandu')),
        ('paingya', _('Paingya')),
        ('parashara', _('Parashara')),
        ('pulaha', _('Pulaha')),
        ('pulastya', _('Pulastya')),
        ('pandya', _('Pandya')),        # Sheet
        ('reva', _('Reva')),
        ('rishyashringa', _('Rishyashringa')),
        ('saandilya', _('Saandilya')),        # Sheet
        ('shaandilya', _('Shaandilya')),
        ('shakalya', _('Shakalya')),
        ('samarayan', _('Samarayan')),        # Sheet
        ('shandilya', _('Shandilya')),
        ('shatamarshana', _('Shatamarshana')),
        ('shaunak', _('Shaunak')),
        ('shukla', _('Shukla')),
        ('srivatsa', _('Srivatsa')),
        ('sutapa', _('Sutapa')),
        ('tiwadi', _('Tiwadi')),        # Sheet
        ('trivadi', _('Trivadi')),        # Sheet
        ('vachchhas', _('Vachchhas')),        # Sheet
        ('vachchhav', _('Vachchhav')),        # Sheet
        ('vadhoola', _('Vadhoola')),
        ('Vashishtha', _('Vasishta')),        # Sheet
        ('vatsat', _('Vatsat')),        # Sheet
        ('vatsa', _('Vatsa')),        # Sheet
        ('vatsak', _('Vatsak')),        # Sheet
        ('vishvamitra', _('Vishvamitra')),
        ('vyas', _('Vyas')),        # Sheet
        ('yajnavalkya', _('Yajnavalkya')),
    ]

    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, related_name='my_family')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    birth_place = models.CharField(max_length=100)
    birth_time = models.TimeField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Height in cm")
    phone_number = models.CharField(max_length=15, unique=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES)
    current_address = models.TextField()
    current_address_village = models.TextField(max_length=100, null=True, blank=True)
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
        ("ba", _("B.A. (Bachelor of Arts)")),
        ("bsc", _("B.Sc. (Bachelor of Science)")),
        ("bcom.", _("B.Com. (Bachelor of Commerce)")),
        ("bba", _("BBA (Bachelor of Business Administration)")),
        ("bca", _("BCA (Bachelor of Computer Applications)")),
        ("btech", _("B.Tech (Bachelor of Technology)")),
        ("be", _("B.E. (Bachelor of Engineering)")),
        ("llb", _("LLB (Bachelor of Laws)")),
        ("mbbs", _("MBBS (Bachelor of Medicine and Bachelor of Surgery)")),
        ("ma", _("M.A. (Master of Arts)")),
        ("msc", _("M.Sc. (Master of Science)")),
        ("mcom", _("M.Com. (Master of Commerce)")),
        ("mba", _("MBA (Master of Business Administration)")),
        ("mca", _("MCA (Master of Computer Applications)")),
        ("mtech", _("M.Tech (Master of Technology)")),
        ("me", _("M.E. (Master of Engineering)")),
        ("llm", _("LLM (Master of Laws)")),
        ("md", _("MD (Doctor of Medicine)")),
        ("diploma", _("Diploma")),
        ("iti", _("ITI (Industrial Training Institute)")),
        ("polytechnic", _("Polytechnic")),
        ("certification", _("Certification Course")),
        ("phd", _("Ph.D. (Doctor of Philosophy)")),
        ("dlitt", _("D.Litt (Doctor of Literature)")),
        ("other", _("Other")),
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
    image = models.ImageField(upload_to='news_events/', help_text="Dimensions of image should be: 730 × 548 px")
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
    class Meta:
        verbose_name_plural = 'Website Suggestions'

    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class Sandesh(models.Model):
    class Meta:
        verbose_name_plural = 'Sandesh'

    sender = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='sandesh_sender')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sandesh_receiver')
    message = models.TextField()
    image = models.FileField(upload_to='sandesh', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class Gallery(models.Model):
    class Meta:
        verbose_name_plural = 'Gallery'

    GALLERY_TYPE_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1980),MaxValueValidator(datetime.date.today().year)],
        help_text=f'year should be between 1980 - {datetime.date.today().year}'
    )
    media_type = models.CharField(max_length=10, choices=GALLERY_TYPE_CHOICES)
    image = models.FileField(upload_to='gallery', null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def get_youtube_embed_url(self):
        if self.video:
            parsed_url = urlparse(f"{self.video}")
            if 'youtube.com' in parsed_url.netloc:
                video_id = parse_qs(parsed_url.query).get('v')
                if video_id:
                    return f'https://www.youtube.com/embed/{video_id[0]}'
            elif 'youtu.be' in parsed_url.netloc:
                return f'https://www.youtube.com/embed/{parsed_url.path.lstrip("/")}'
        return None

    def __str__(self):
        return self.title

    def clean(self, scheduled=False):
        super().clean()
        if self.media_type == 'photo' and not self.image:
            raise ValidationError({
                'image': "You must upload an image if 'Photo' is selected as media type.",
            })
        elif self.media_type == 'video' and not self.video:
            raise ValidationError({
                'video': "You must enter a YouTube video URL if 'Video' is selected as media type.",
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Culture(models.Model):
    class Meta:
        verbose_name_plural = 'Culture'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)