from django.db import models


class FamilyMember(models.Model):
    family_id = models.IntegerField()
    name = models.CharField(max_length=255)
    gotra = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    relation_with_head = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
