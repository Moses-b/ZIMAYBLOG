from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from zimayblog.localization import get_language, get_ui_text
from .models import BlogComment, BlogContribution
from .services import get_public_post_by_slug, get_public_posts


def blog_list(request):
    language = get_language(request)
    ui = get_ui_text(language)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        contribution_type = request.POST.get("contribution_type", BlogContribution.ARTICLE).strip()
        category = request.POST.get("category", "").strip()
        title = request.POST.get("title", "").strip()
        excerpt = request.POST.get("excerpt", "").strip()
        content = request.POST.get("content", "").strip()

        if name and email and content:
            if contribution_type == BlogContribution.ARTICLE and not title:
                messages.error(request, ui["contribution_error"])
                return redirect("app:blog_list")

            BlogContribution.objects.create(
                contribution_type=contribution_type,
                name=name,
                email=email,
                category=category,
                title=title,
                excerpt=excerpt,
                content=content,
            )
            messages.success(request, ui["contribution_success"])
            return redirect("app:blog_list")

        messages.error(request, ui["contribution_error"])
        return redirect("app:blog_list")

    return render(
        request,
        "blog/list.html",
        {
            "posts": get_public_posts(language),
            "ui": ui,
            "current_language": language,
        },
    )


def blog_detail(request, slug):
    language = get_language(request)
    ui = get_ui_text(language)
    post = get_public_post_by_slug(slug, language)
    if not post:
        raise Http404("Article not found")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        content = request.POST.get("content", "").strip()
        if name and email and content:
            BlogComment.objects.create(
                post_slug=slug,
                name=name,
                email=email,
                content=content,
                is_visible=True,
            )
            messages.success(request, ui["article_comment_success"])
        else:
            messages.error(request, ui["article_comment_error"])
        return redirect("app:blog_detail", slug=slug)

    comments = BlogComment.objects.filter(post_slug=slug, is_visible=True)
    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "comments": comments,
            "ui": ui,
            "current_language": language,
            "featured_video": {
                "title": "Free Courses Library" if language == "en" else "Bibliotheque de cours gratuits",
                "summary": "Access curated courses by category after login." if language == "en" else "Accedez aux cours par categorie apres connexion.",
                "url": "/courses/",
                "label": "Free Courses" if language == "en" else "Cours Gratuits",
                "placeholder": False,
            },
        },
    )
