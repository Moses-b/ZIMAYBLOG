from django.test import TestCase
from django.urls import reverse

from .models import ContactLead


class HomeContactFormTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Build a stronger business")

    def test_contact_submission_creates_lead(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Test Client",
                "email": "client@example.com",
                "service": "Website creation",
                "message": "Need a premium website.",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactLead.objects.count(), 1)
        self.assertContains(response, "Your request has been received")
