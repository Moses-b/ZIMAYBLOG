from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    BlogContribution,
    BlogComment,
    BlogPost,
    ContactLead,
    CourseCategory,
    CourseComment,
    CourseCommentLike,
    CourseProgress,
    CourseSubcategory,
    CourseVideo,
    DiplomaCategory,
    Diploma,
    ProjectItem,
    normalize_youtube_url,
)


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "source", "created_at")
    search_fields = ("name", "email", "service", "message")
    list_filter = ("service", "source", "created_at")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "is_published", "published_at", "created_at")
    search_fields = ("title", "category", "excerpt", "content", "author_name", "author_email")
    list_filter = ("is_published", "category", "created_at", "published_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogContribution)
class BlogContributionAdmin(admin.ModelAdmin):
    list_display = ("title", "contribution_type", "name", "email", "is_approved", "approved_at", "created_at")
    search_fields = ("title", "name", "email", "category", "excerpt", "content")
    list_filter = ("contribution_type", "is_approved", "created_at", "approved_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post_slug", "is_visible", "created_at")
    search_fields = ("name", "email", "post_slug", "content")
    list_filter = ("is_visible", "created_at")
    ordering = ("-created_at",)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name", "slug")
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CourseSubcategory)
class CourseSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "order")
    search_fields = ("name", "slug", "category__name")
    ordering = ("category", "order", "name")
    prepopulated_fields = {"slug": ("name",)}


class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["youtube_url"].help_text = (
            "Paste the full YouTube embed iframe here (e.g. "
            '<iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>). '
            "We will extract the src automatically."
        )

    def clean_youtube_url(self):
        value = self.cleaned_data.get("youtube_url", "")
        return normalize_youtube_url(value)


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    form = CourseVideoForm
    list_display = ("title", "category", "subcategory", "is_published", "order", "created_at")
    search_fields = ("title", "youtube_url", "description", "category__name", "subcategory__name")
    list_filter = ("is_published", "category", "subcategory")
    ordering = ("order", "-created_at")
    readonly_fields = ("embed_preview", "embed_requirements")
    fields = (
        "category",
        "subcategory",
        "title",
        "youtube_url",
        "embed_preview",
        "embed_requirements",
        "description",
        "is_published",
        "order",
    )

    @admin.display(description="Embed preview")
    def embed_preview(self, obj):
        if not obj or not obj.youtube_url:
            return "Save this video to load the preview."
        src = normalize_youtube_url(obj.youtube_url)
        return format_html(
            '<iframe width="420" height="236" src="{}" title="Embed preview" frameborder="0" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
            src,
        )

    @admin.display(description="Embed requirements")
    def embed_requirements(self, obj):
        return (
            "If the preview shows 'Video unavailable', check YouTube Studio settings: "
            "Allow embedding enabled, visibility Public/Unlisted, and no restrictions blocking embed."
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.warning(
            request,
            "If your site still shows 'Video unavailable', enable 'Allow embedding' in YouTube Studio for this video.",
        )


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "is_watched", "updated_at")
    search_fields = ("user__username", "video__title")
    list_filter = ("is_watched", "updated_at")


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "created_at")
    search_fields = ("user__username", "video__title", "content")
    list_filter = ("created_at",)


@admin.register(CourseCommentLike)
class CourseCommentLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created_at")
    search_fields = ("user__username", "comment__content")
    list_filter = ("created_at",)


@admin.register(Diploma)
class DiplomaAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "issuer", "date_label", "is_published", "created_at")
    search_fields = ("title", "issuer", "summary", "image_source", "certificate_source")
    list_filter = ("category", "is_published", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("image_preview",)
    fields = (
        "category",
        "title",
        "issuer",
        "date_label",
        "summary",
        "image_source",
        "image_preview",
        "certificate_source",
        "cta_label",
        "is_published",
    )

    @admin.display(description="Image preview")
    def image_preview(self, obj):
        if not obj:
            return "Save first to preview."
        if not obj.image_url:
            return "No image URL."
        return format_html(
            '<img src="{}" alt="Diploma preview" style="max-width:360px;border-radius:12px;border:1px solid #23364d;" />',
            obj.image_url,
        )


@admin.register(DiplomaCategory)
class DiplomaCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name", "slug")
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "order", "created_at")
    search_fields = ("title", "summary", "description", "slug")
    list_filter = ("category", "is_published", "created_at")
    ordering = ("order", "-created_at")
    prepopulated_fields = {"slug": ("title",)}
