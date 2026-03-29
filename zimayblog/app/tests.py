from django.test import TestCase
from django.urls import reverse

from .models import BlogComment, BlogContribution, BlogPost, ContactLead


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


class BlogPublishingTests(TestCase):
    def test_admin_blog_post_can_be_listed_publicly_when_published(self):
        post = BlogPost.objects.create(
            category="Finance",
            title="Admin published article",
            excerpt="Published from the admin.",
            content="First paragraph.\n\nSecond paragraph.",
            is_published=True,
        )
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        detail = self.client.get(reverse("blog:blog_detail", args=[post.slug]))
        self.assertContains(detail, post.title)

    def test_visitor_article_requires_admin_approval_before_publication(self):
        response = self.client.post(
            reverse("blog:blog_list"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "contribution_type": "article",
                "category": "Community",
                "title": "Visitor contribution",
                "excerpt": "Short summary",
                "content": "A community article waiting for approval.",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        contribution = BlogContribution.objects.get(email="visitor@example.com")
        self.assertFalse(contribution.is_approved)
        self.assertContains(response, "awaiting admin review")
        listing = self.client.get(reverse("blog:blog_list"))
        self.assertNotContains(listing, "Visitor contribution")

    def test_approved_visitor_article_becomes_public(self):
        contribution = BlogContribution.objects.create(
            contribution_type=BlogContribution.ARTICLE,
            name="Visitor",
            email="visitor@example.com",
            category="Community",
            title="Approved visitor article",
            excerpt="Approved summary",
            content="Approved content for the public blog.",
            is_approved=True,
        )
        response = self.client.get(reverse("blog:blog_list"))
        self.assertContains(response, contribution.title)
        detail = self.client.get(reverse("blog:blog_detail", args=[contribution.slug]))
        self.assertContains(detail, contribution.title)

    def test_visitors_can_comment_under_blog_article(self):
        post = BlogPost.objects.create(
            category="Finance",
            title="Commentable article",
            excerpt="Comment test",
            content="Paragraph one.",
            is_published=True,
        )
        response = self.client.post(
            reverse("blog:blog_detail", args=[post.slug]),
            {
                "name": "Visitor Name",
                "email": "visitor@example.com",
                "content": "Very useful article!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BlogComment.objects.filter(post_slug=post.slug).count(), 1)
        self.assertContains(response, "Very useful article!")
