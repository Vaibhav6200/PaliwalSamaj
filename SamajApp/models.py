from django.db import models
import uuid
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
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
    ]

    QUALIFICATION_CHOICES = [
        ('school', 'School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
    ]

    OCCUPATION_CHOICES = [
        ('job', 'Job'),
        ('business', 'Business'),
    ]
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, related_name='my_family')
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    birth_place = models.CharField(max_length=100)
    birth_time = models.TimeField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    gotra = models.CharField(max_length=100)
    current_address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    qualification_type = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    occupation_type = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class QualificationDetail(models.Model):
    class Meta:
        verbose_name_plural = 'Qualification Details'

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='qualification_detail')
    class_name = models.CharField(max_length=20, blank=True, null=True)  # Only if School
    college_name = models.CharField(max_length=100, blank=True, null=True)  # For UG/Graduate
    degree_name = models.CharField(max_length=100, blank=True, null=True)  # For UG/Graduate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Qualification for {self.member.name}"


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
        return f"Occupation for {self.member.name}"


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
