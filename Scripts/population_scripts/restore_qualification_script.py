import json
import os
import sys
import random

from django.db import IntegrityError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
import django

django.setup()

from SamajApp.models import QualificationDetail


def restore_script():
    # Load full dump
    with open("data.json") as f:
        data = json.load(f)

    # Filter only QualificationDetail
    qualification_data = [
        entry for entry in data if entry["model"] == "SamajApp.qualificationdetail"
    ]

    # Save to a new JSON
    with open("qualification_restore.json", "w") as f:
        json.dump(qualification_data, f, indent=2)

if __name__ == "__main__":
    restore_script()
    print("Qualifications Restored Successfully.")
