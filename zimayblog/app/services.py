from django.utils import timezone

from .content import get_posts as get_static_posts
from .models import BlogContribution, BlogPost


def split_paragraphs(content):
    return [paragraph.strip() for paragraph in content.split("\n\n") if paragraph.strip()]


def estimate_read_time(content):
    words = max(len(content.split()), 1)
    minutes = max(1, round(words / 180))
    return f"{minutes} min read"


def format_month_date(value, language):
    if not value:
        return ""
    if language == "fr":
        months = {
            1: "janvier",
            2: "fevrier",
            3: "mars",
            4: "avril",
            5: "mai",
            6: "juin",
            7: "juillet",
            8: "aout",
            9: "septembre",
            10: "octobre",
            11: "novembre",
            12: "decembre",
        }
        return f"{months[value.month]} {value.year}"
    return value.strftime("%B %Y")


def serialize_blog_post(post, language):
    published_on = post.published_at or post.created_at or timezone.now()
    return {
        "id": f"db-{post.pk}",
        "slug": post.slug,
        "category": post.category,
        "title": post.title,
        "excerpt": post.excerpt,
        "read_time": estimate_read_time(post.content),
        "date": format_month_date(published_on, language),
        "content": split_paragraphs(post.content),
        "author_name": post.author_name,
        "author_email": post.author_email,
        "is_community": False,
        "published_on": published_on,
    }


def serialize_contribution(contribution, language):
    published_on = contribution.approved_at or contribution.created_at or timezone.now()
    return {
        "id": f"community-{contribution.pk}",
        "slug": contribution.slug,
        "category": contribution.category or "Community",
        "title": contribution.title,
        "excerpt": contribution.excerpt,
        "read_time": estimate_read_time(contribution.content),
        "date": format_month_date(published_on, language),
        "content": split_paragraphs(contribution.content),
        "author_name": contribution.name,
        "author_email": contribution.email,
        "is_community": True,
        "published_on": published_on,
    }


def get_public_posts(language):
    static_posts = list(get_static_posts(language))
    blog_posts = [
        serialize_blog_post(post, language)
        for post in BlogPost.objects.filter(is_published=True)
    ]
    community_posts = [
        serialize_contribution(contribution, language)
        for contribution in BlogContribution.objects.filter(
            contribution_type=BlogContribution.ARTICLE,
            is_approved=True,
        )
    ]
    dynamic_posts = sorted(
        blog_posts + community_posts,
        key=lambda item: item["published_on"],
        reverse=True,
    )
    return dynamic_posts + static_posts


def get_public_post_by_slug(slug, language):
    blog_post = BlogPost.objects.filter(slug=slug, is_published=True).first()
    if blog_post:
        return serialize_blog_post(blog_post, language)

    contribution = BlogContribution.objects.filter(
        slug=slug,
        contribution_type=BlogContribution.ARTICLE,
        is_approved=True,
    ).first()
    if contribution:
        return serialize_contribution(contribution, language)

    return next((item for item in get_static_posts(language) if item["slug"] == slug), None)
