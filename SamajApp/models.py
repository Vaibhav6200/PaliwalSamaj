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


class State(models.Model):
    class Meta:
        verbose_name_plural = 'States'

    state_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.state_name


class City(models.Model):
    class Meta:
        verbose_name_plural = 'Cities'
        unique_together = ('city_name', 'state')

    city_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.city_name}"


class Village(models.Model):
    class Meta:
        verbose_name_plural = 'Villages'
        unique_together = ('village_name', 'city')

    village_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='villages')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.village_name}"


class Family(models.Model):
    class Meta:
        verbose_name_plural = 'Family'

    name = models.CharField(max_length=100)  # e.g., Sharma
    family_code = models.CharField(max_length=30, unique=True, editable=False)
    family_head = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_family')
    paitrik_address = models.CharField(max_length=255, null=True, blank=True)
    paitrik_address_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL)
    paitrik_address_city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    paitrik_address_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
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
        ('student', _("Student")),
        ('retired', _("Retired")),
        ('housewife', _("Housewife"))
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, null=True, blank=True)
    birth_time = models.TimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Height in cm")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES, null=True, blank=True)

    # Member Current Address Details
    current_address = models.CharField(max_length=255, null=True, blank=True)
    current_address_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    current_address_city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    current_address_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL)
    current_address_pincode = models.CharField(max_length=10, null=True, blank=True)

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    qualification_type = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, null=True, blank=True)
    occupation_type = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default='none')
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user}"


class Degree(models.Model):
    degree_code = models.CharField(max_length=50, unique=True)   # e.g. "bsc", "mba"
    degree_name = models.CharField(max_length=255)              # e.g. "B.Sc. (Bachelor of Science)"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Degree"
        verbose_name_plural = "Degrees"
        ordering = ["degree_name"]

    def __str__(self):
        return self.degree_name


class QualificationDetail(models.Model):
    class Meta:
        verbose_name_plural = 'Qualification Details'

    DEGREE_CHOICES = [
        # Undergraduate Degrees
        ("ba", _("B.A. (Bachelor of Arts)")),
        ("bsc", _("B.Sc. (Bachelor of Science)")),
        ("bcom", _("B.Com. (Bachelor of Commerce)")),
        ("bba", _("BBA (Bachelor of Business Administration)")),
        ("bbm", _("BBM (Bachelor of Business Management)")),
        ("bca", _("BCA (Bachelor of Computer Applications)")),
        ("bcis", _("BCIS (Bachelor of Computer Information Systems)")),
        ("bpharma", _("B.Pharma (Bachelor of Pharmacy)")),
        ("btech", _("B.Tech (Bachelor of Technology)")),
        ("be", _("B.E. (Bachelor of Engineering)")),
        ("bjmc", _("BJMC (Bachelor of Journalism and Mass Communication)")),
        ("bms", _("BMS (Bachelor of Management Studies)")),
        ("bds", _("BDS (Bachelor of Dental Surgery)")),
        ("bhms", _("BHMS (Bachelor of Homeopathic Medicine & Surgery)")),
        ("barch", _("B.Arch (Bachelor of Architecture)")),
        ("bpt", _("BPT (Bachelor of Physiotherapy)")),
        ("llb", _("LLB (Bachelor of Laws)")),
        ("bped", _("B.P.Ed (Bachelor of Physical Education)")),
        ("blisc", _("B.Lib.I.Sc (Bachelor of Library & Information Science)")),
        ("bse", _("BSE (Bachelor of Science in Education)")),
        ("mbbs", _("MBBS (Bachelor of Medicine & Surgery)")),
        ("bams", _("BAMS (Bachelor of Ayurvedic Medicine & Surgery)")),
        ("bvsc", _("BVSc (Bachelor of Veterinary Science)")),

        # Professional Courses
        ("ca", _("CA (Chartered Accountant)")),
        ("cs", _("CS (Company Secretary)")),
        ("cfa", _("CFA (Chartered Financial Analyst)")),
        ("fca", _("FCA (Fellow Chartered Accountant)")),
        ("mfc", _("MFC (Master of Finance and Control)")),

        # Postgraduate Degrees
        ("ma", _("M.A. (Master of Arts)")),
        ("msc", _("M.Sc. (Master of Science)")),
        ("mcom", _("M.Com. (Master of Commerce)")),
        ("mba", _("MBA (Master of Business Administration)")),
        ("mca", _("MCA (Master of Computer Applications)")),
        ("mtech", _("M.Tech (Master of Technology)")),
        ("mhrm", _("MHRM (Master of Human Resource Management)")),
        ("mphil", _("M.Phil. (Master of Philosophy)")),
        ("me", _("M.E. (Master of Engineering)")),
        ("ms", _("MS (Master of Science)")),
        ("med", _("M.Ed (Master of Education)")),
        ("mpharma", _("M.Pharma (Master of Pharmacy)")),
        ("msw", _("MSW (Master of Social Work)")),
        ("llm", _("LLM (Master of Laws)")),

        # Doctorate & Super-specializations
        ("dlitt", _("D.Litt (Doctor of Literature)")),
        ("phd", _("Ph.D. (Doctor of Philosophy)")),
        ("mch", _("M.Ch (Magister Chirurgiae / Master of Surgery)")),
        ("md", _("MD (Doctor of Medicine)")),
        ("pediatrician", _("Pediatrician")),

        # Medical PG & Super-specialty
        ("dm", _("DM (Doctorate of Medicine)")),
        ("dnb", _("DNB (Diplomate of National Board)")),

        # Diplomas & Certificates
        ("bed", _("B.Ed (Bachelor of Education)")),
        ("pgdca", _("PGDCA (Post Graduate Diploma in Computer Applications)")),
        ("iti", _("ITI (Industrial Training Institute)")),
        ("polytechnic", _("Polytechnic")),
        ("stenography", _("Stenography")),
        ("pgdc", _("PGDC (Post Graduate Diploma in Computer)")),
        ("pgdll", _("PGDLL (Post Graduate Diploma in Labour Laws)")),
        ("dca", _("DCA (Diploma in Computer Applications)")),
        ("dll", _("DLL (Diploma in Labour Laws)")),
        ("dllb", _("DLLB (Diploma in Law)")),
        ("bstc", _("BSTC (Basic School Teaching Certificate)")),
        ("stc", _("STC (School Teaching Certificate)")),

        # Extras
        ("blisc", _("B.Lib.I.Sc (Bachelor of Library & Information Science)")),
        ("nursery", _("Nursery")),
        ("uneducated", _("Uneducated")),
        ("primary", _("Primary Education")),
        ("secondary", _("Secondary (10th)")),
        ("ssc", _("SSC (10th Grade)")),
        ("puc", _("PUC / HSC / 12th Grade")),
        ("bpt", _("Bachelor of Physiotherapy")),
        ("Yoga", _("Yoga")),

        # Other
        ("other", _("Other")),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='qualification_detail')
    school_class = models.PositiveSmallIntegerField(blank=True, null=True)  # Only if School
    school_name = models.CharField(max_length=255, blank=True, null=True)
    college_name = models.CharField(max_length=100, blank=True, null=True)  # For UG/Graduate
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, null=True, blank=True)
    other_degree_text = models.CharField(max_length=255, null=True, blank=True)
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
        return f"Occupation for {self.member}"


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


class DisplayMemberGroup(models.Model):
    class Meta:
        verbose_name_plural = 'Display Groups'

    group_name = models.CharField(max_length=255)
    group_rank = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.group_name}"


class DisplayMember(models.Model):
    class Meta:
        verbose_name_plural = 'Display Members'

    ROLE_CHOICES = [
        ('adhyaksh', _('Adhyaksh')),
        ('upadhyaksh', _('Upadhyaksh')),
        ('sachiv', _('Sachiv')),
        ('sanrakshak', _('Sanrakshak')),
        ('mahila_adhyaksh', _('Mahila Adhyaksh')),
        ('koshadhyaksh', _('Koshadhyaksh')),
        ('saha_sachiv', _('Saha Sachiv')),
        ('salahkaar', _('Salahkaar')),
        ('aayojan_samiti', _('Aayojan Samiti')),
        ('karyakari_sadasya', _('Karyakari Sadasya')),
    ]
    group = models.ForeignKey(DisplayMemberGroup, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    member_image = models.FileField(upload_to='samaj_display_members', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    rank = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.member_name} - {self.role}"


class Suggestion(models.Model):
    class Meta:
        verbose_name_plural = 'Website Suggestions'

    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
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
    rank = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    pdf_flag = models.BooleanField(default=False)
    pdf = models.FileField(upload_to='culture_pdf', null=True, blank=True)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Update Slug
        self.slug = slugify(self.title)
        # Update Rank
        if not self.pk and (self.rank is None or self.rank == 10):  # new object & no custom rank
            max_rank = Culture.objects.aggregate(models.Max('rank'))['rank__max'] or 0
            self.rank = max_rank + 10
        super().save(*args, **kwargs)


class SponsorAd(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='ads/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        print(f"[DEBUG] name: {self.name}, image: {self.image}, image.name: {getattr(self.image, 'name', None)}")

        if self.name:
            return self.name
        elif self.image:
            return self.image.name.split('/')[-1]
        return 'unnamed ad'

    def clean(self, scheduled=False):
        super().clean()
        if self.is_active:
            SponsorAd.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SMSLog(models.Model):
    member = models.ForeignKey("Member", on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    reference_id = models.CharField(max_length=50, null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"SMS to {self.phone_number}"


class Support(models.Model):
    class Meta:
        verbose_name_plural = 'Support'
    full_name = models.CharField(max_length=255)
    email = models.TextField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.BooleanField(default=False, help_text='True: Mark as resolved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.full_name}"