import os
import sys
import random

from django.db import IntegrityError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')
import django

django.setup()

from SamajApp.models import Degree

DEGREE_CHOICES = [
    # Undergraduate Degrees
    ("ba", "B.A. (Bachelor of Arts)", "बी.ए. (बैचलर ऑफ आर्ट्स)"),
    ("bsc", "B.Sc. (Bachelor of Science)", "बी.एससी. (बैचलर ऑफ साइंस)"),
    ("bcom", "B.Com. (Bachelor of Commerce)", "बी.कॉम. (बैचलर ऑफ कॉमर्स)"),
    ("bba", "BBA (Bachelor of Business Administration)", "बीबीए (बैचलर ऑफ बिज़नेस एडमिनिस्ट्रेशन)"),
    ("bbm", "BBM (Bachelor of Business Management)", "बीबीएम (बैचलर ऑफ बिज़नेस मैनेजमेंट)"),
    ("bca", "BCA (Bachelor of Computer Applications)", "बीसीए (बैचलर ऑफ कंप्यूटर एप्लिकेशन्स)"),
    ("bcis", "BCIS (Bachelor of Computer Information Systems)", "बीसीआईएस (बैचलर ऑफ कंप्यूटर इन्फ़ॉर्मेशन सिस्टम्स)"),
    ("bpharma", "B.Pharma (Bachelor of Pharmacy)", "बी.फार्मा (बैचलर ऑफ फार्मेसी)"),
    ("btech", "B.Tech (Bachelor of Technology)", "बी.टेक (बैचलर ऑफ टेक्नोलॉजी)"),
    ("be", "B.E. (Bachelor of Engineering)", "बी.ई. (बैचलर ऑफ इंजीनियरिंग)"),
    ("bjmc", "BJMC (Bachelor of Journalism and Mass Communication)", "बीजेएमसी (बैचलर ऑफ जर्नलिज़्म एंड मास कम्युनिकेशन)"),
    ("bms", "BMS (Bachelor of Management Studies)", "बीएमएस (बैचलर ऑफ मैनेजमेंट स्टडीज़)"),
    ("bds", "BDS (Bachelor of Dental Surgery)", "बीडीएस (बैचलर ऑफ डेंटल सर्जरी)"),
    ("bhms", "BHMS (Bachelor of Homeopathic Medicine & Surgery)", "बीएचएमएस (बैचलर ऑफ होम्योपैथिक मेडिसिन एंड सर्जरी)"),
    ("barch", "B.Arch (Bachelor of Architecture)", "बी.आर्क (बैचलर ऑफ आर्किटेक्चर)"),
    ("bpt", "BPT (Bachelor of Physiotherapy)", "बीपीटी (बैचलर ऑफ फिज़ियोथेरेपी)"),
    ("llb", "LLB (Bachelor of Laws)", "एलएलबी (बैचलर ऑफ लॉज़)"),
    ("bped", "B.P.Ed (Bachelor of Physical Education)", "बी.पी.एड (बैचलर ऑफ फ़िज़िकल एजुकेशन)"),
    ("blisc", "B.Lib.I.Sc (Bachelor of Library & Information Science)", "बी.लिब.आई.एससी (बैचलर ऑफ लाइब्रेरी एंड इन्फ़ॉर्मेशन साइंस)"),
    ("bse", "BSE (Bachelor of Science in Education)", "बीएसई (बैचलर ऑफ साइंस इन एजुकेशन)"),
    ("mbbs", "MBBS (Bachelor of Medicine & Surgery)", "एमबीबीएस (बैचलर ऑफ मेडिसिन एंड सर्जरी)"),
    ("bams", "BAMS (Bachelor of Ayurvedic Medicine & Surgery)", "बीएएमएस (बैचलर ऑफ आयुर्वेदिक मेडिसिन एंड सर्जरी)"),
    ("bvsc", "BVSc (Bachelor of Veterinary Science)", "बीवीएससी (बैचलर ऑफ वेटेरिनरी साइंस)"),

    # Professional Courses
    ("ca", "CA (Chartered Accountant)", "सीए (चार्टर्ड अकाउंटेंट)"),
    ("cs", "CS (Company Secretary)", "सीएस (कंपनी सेक्रेटरी)"),
    ("cfa", "CFA (Chartered Financial Analyst)", "सीएफए (चार्टर्ड फ़ाइनेंशियल एनालिस्ट)"),
    ("fca", "FCA (Fellow Chartered Accountant)", "एफसीए (फेलो चार्टर्ड अकाउंटेंट)"),
    ("mfc", "MFC (Master of Finance and Control)", "एमएफसी (मास्टर ऑफ फ़ाइनेंस एंड कंट्रोल)"),

    # Postgraduate Degrees
    ("ma", "M.A. (Master of Arts)", "एम.ए. (मास्टर ऑफ आर्ट्स)"),
    ("msc", "M.Sc. (Master of Science)", "एम.एससी. (मास्टर ऑफ साइंस)"),
    ("mcom", "M.Com. (Master of Commerce)", "एम.कॉम. (मास्टर ऑफ कॉमर्स)"),
    ("mba", "MBA (Master of Business Administration)", "एमबीए (मास्टर ऑफ बिज़नेस एडमिनिस्ट्रेशन)"),
    ("mca", "MCA (Master of Computer Applications)", "एमसीए (मास्टर ऑफ कंप्यूटर एप्लिकेशन्स)"),
    ("mtech", "M.Tech (Master of Technology)", "एम.टेक (मास्टर ऑफ टेक्नोलॉजी)"),
    ("mhrm", "MHRM (Master of Human Resource Management)", "एमएचआरएम (मास्टर ऑफ ह्यूमन रिसोर्स मैनेजमेंट)"),
    ("mphil", "M.Phil. (Master of Philosophy)", "एम.फिल. (मास्टर ऑफ फिलॉसफी)"),
    ("me", "M.E. (Master of Engineering)", "एम.ई. (मास्टर ऑफ इंजीनियरिंग)"),
    ("ms", "MS (Master of Science)", "एमएस (मास्टर ऑफ साइंस)"),
    ("med", "M.Ed (Master of Education)", "एम.एड (मास्टर ऑफ एजुकेशन)"),
    ("mpharma", "M.Pharma (Master of Pharmacy)", "एम.फार्मा (मास्टर ऑफ फार्मेसी)"),
    ("msw", "MSW (Master of Social Work)", "एमएसडब्ल्यू (मास्टर ऑफ सोशल वर्क)"),
    ("llm", "LLM (Master of Laws)", "एलएलएम (मास्टर ऑफ लॉज़)"),

    # Doctorate & Super-specializations
    ("dlitt", "D.Litt (Doctor of Literature)", "डी.लिट्ट (डॉक्टर ऑफ लिटरेचर)"),
    ("phd", "Ph.D. (Doctor of Philosophy)", "पीएचडी (डॉक्टर ऑफ फिलॉसफी)"),
    ("mch", "M.Ch (Magister Chirurgiae / Master of Surgery)", "एम.च (मजिस्टर सर्जरी/ मास्टर ऑफ सर्जरी)"),
    ("md", "MD (Doctor of Medicine)", "एमडी (डॉक्टर ऑफ मेडिसिन)"),
    ("pediatrician", "Pediatrician", "पीडियाट्रिशियन"),

    # Medical PG & Super-specialty
    ("dm", "DM (Doctorate of Medicine)", "डीएम (डॉक्टरेट ऑफ मेडिसिन)"),
    ("dnb", "DNB (Diplomate of National Board)", "डीएनबी (डिप्लोमेट ऑफ नेशनल बोर्ड)"),

    # Diplomas & Certificates
    ("bed", "B.Ed (Bachelor of Education)", "बी.एड (बैचलर ऑफ एजुकेशन)"),
    ("pgdca", "PGDCA (Post Graduate Diploma in Computer Applications)", "पीजीडीसीए (पोस्ट ग्रेजुएट डिप्लोमा इन कंप्यूटर एप्लिकेशन्स)"),
    ("iti", "ITI (Industrial Training Institute)", "आईटीआई (इंडस्ट्रियल ट्रेनिंग इंस्टिट्यूट)"),
    ("polytechnic", "Polytechnic", "पॉलीटेक्निक"),
    ("stenography", "Stenography", "स्टेनोग्राफी"),
    ("pgdc", "PGDC (Post Graduate Diploma in Computer)", "पीजीडीसी (पोस्ट ग्रेजुएट डिप्लोमा इन कंप्यूटर)"),
    ("pgdll", "PGDLL (Post Graduate Diploma in Labour Laws)", "पीजीडीएलएल (पोस्ट ग्रेजुएट डिप्लोमा इन लेबर लॉज़)"),
    ("dca", "DCA (Diploma in Computer Applications)", "डीसीए (डिप्लोमा इन कंप्यूटर एप्लिकेशन्स)"),
    ("dll", "DLL (Diploma in Labour Laws)", "डीएलएल (डिप्लोमा इन लेबर लॉज़)"),
    ("dllb", "DLLB (Diploma in Law)", "डीएलएलबी (डिप्लोमा इन लॉ)"),
    ("bstc", "BSTC (Basic School Teaching Certificate)", "बीएसटीसी (बेसिक स्कूल टीचिंग सर्टिफिकेट)"),
    ("stc", "STC (School Teaching Certificate)", "एसटीसी (स्कूल टीचिंग सर्टिफिकेट)"),

    # Extras
    ("nursery", "Nursery", "नर्सरी"),
    ("uneducated", "Uneducated", "अशिक्षित"),
    ("primary", "Primary Education", "प्राथमिक शिक्षा"),
    ("secondary", "Secondary (10th)", "सेकेंडरी (10वीं)"),
    ("ssc", "SSC (10th Grade)", "एसएससी (10वीं कक्षा)"),
    ("puc", "PUC / HSC / 12th Grade", "पीयूसी / एचएससी / 12वीं कक्षा"),
    ("Yoga", "Yoga", "योग"),

    # Other
    ("other", "Other", "अन्य"),
]


def populate_degree_modal():
    for deg_code, deg_en, deg_hi in DEGREE_CHOICES:
        try:
            obj, created = Degree.objects.get_or_create(
                degree_code=deg_code,
                defaults={"degree_name": deg_en, "degree_name_en": deg_en, 'degree_name_hi': deg_hi}
            )
            if created:
                print(f"✅ Created: {deg_code} - {deg_en} - {deg_hi}")
            else:
                print(f"ℹ️ Already exists: {deg_code} - {deg_en} - {deg_hi}")
        except IntegrityError as e:
            print(f"❌ UNIQUE constraint failed for: {deg_code} - {deg_en} - {deg_hi} ({e})")

if __name__ == "__main__":
    populate_degree_modal()
    print("Degree Modal Populated successfully.")
