from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import BankProfile, Vacancy, Application

class RecruitmentDemoFlowTests(TestCase):
    def setUp(self):
        self.bank = BankProfile.objects.create(
            name="Sample Test Finance Bank", short_name="STFB",
            primary_color="#12345b", accent_color="#c49a52"
        )
        self.vacancy = Vacancy.objects.create(
            bank=self.bank, title="Demo Associate", description="Test role",
            closing_date=timezone.localdate() + timedelta(days=20)
        )

    def test_homepage_and_vacancies_render(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("vacancies")).status_code, 200)

    def test_application_submission_and_pdf_receipt(self):
        payload = {
            "full_name": "Test Applicant",
            "date_of_birth": "1998-04-12",
            "gender": "Prefer not to say",
            "city": "Test City",
            "state": "Test State",
            "postal_code": "000000",
            "country": "India",
            "email": "test@example.invalid",
            "phone": "0000000000",
            "qualification": "Graduation",
            "institution": "Test Institute",
            "passing_year": "2020",
            "grade": "A",
            "employment_status": "Fresher",
            "experience": "",
            "organization": "",
            "skills": "Testing",
            "demo_acknowledged": "on",
        }
        response = self.client.post(reverse("apply", args=[self.vacancy.id]), payload)
        self.assertEqual(response.status_code, 302)
        application = Application.objects.get()
        confirmation = self.client.get(reverse("confirmation", args=[application.reference]))
        self.assertEqual(confirmation.status_code, 200)
        pdf = self.client.get(reverse("receipt_pdf", args=[application.reference]))
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))
