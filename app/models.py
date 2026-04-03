from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.templatetags.static import static
from urllib.parse import parse_qs, urlparse
import re
from django.utils import timezone
from django.utils.text import slugify


class ContactLead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    service = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=50, default="website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class BlogPost(models.Model):
    category = models.CharField(max_length=120)
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    excerpt = models.TextField(max_length=420)
    content = models.TextField(help_text="Use blank lines to separate paragraphs.")
    author_name = models.CharField(max_length=150, blank=True)
    author_email = models.EmailField(blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        if not self.is_published:
            self.published_at = None
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)[:220] or "blog-post"
        slug = base_slug
        counter = 2
        while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug[:220-len(str(counter))-1]}-{counter}"
            counter += 1
        return slug


class BlogContribution(models.Model):
    ARTICLE = "article"
    SUGGESTION = "suggestion"
    CONTRIBUTION_TYPES = [
        (ARTICLE, "Article"),
        (SUGGESTION, "Suggestion"),
    ]

    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES, default=ARTICLE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    category = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=220, blank=True)
    slug = models.SlugField(max_length=240, unique=True, blank=True, null=True)
    excerpt = models.TextField(max_length=420, blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        label = self.title or self.get_contribution_type_display()
        return f"{label} - {self.email}"

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = self._generate_unique_slug()
        if self.is_approved and not self.approved_at:
            self.approved_at = timezone.now()
        if not self.is_approved:
            self.approved_at = None
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)[:220] or "community-post"
        slug = base_slug
        counter = 2
        while BlogContribution.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug[:220-len(str(counter))-1]}-{counter}"
            counter += 1
        return slug


class BlogComment(models.Model):
    post_slug = models.SlugField(max_length=240, db_index=True)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    content = models.TextField()
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} on {self.post_slug}"


class CourseCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140] or "course-category"
        super().save(*args, **kwargs)


class CourseSubcategory(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        unique_together = ("category", "slug")

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140] or "course-subcategory"
        super().save(*args, **kwargs)


class CourseVideo(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="videos")
    subcategory = models.ForeignKey(
        CourseSubcategory, on_delete=models.SET_NULL, related_name="videos", null=True, blank=True
    )
    title = models.CharField(max_length=220)
    youtube_url = models.TextField()
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.youtube_url = normalize_youtube_url(self.youtube_url)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.youtube_url:
            raise ValidationError({"youtube_url": "This field is required."})
        normalized = normalize_youtube_url(self.youtube_url)
        if not normalized or "/embed/" not in normalized:
            raise ValidationError({"youtube_url": "Please paste a valid YouTube embed iframe or embed URL."})
        self.youtube_url = normalized


class Diploma(models.Model):
    class SourceType(models.TextChoices):
        STATIC = "static", "Static file path"
        URL = "url", "External URL"

    category = models.ForeignKey(
        "DiplomaCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diplomas",
    )
    title = models.CharField(max_length=220)
    issuer = models.CharField(max_length=220)
    date_label = models.CharField(max_length=60, blank=True)
    summary = models.TextField(blank=True)
    image_source = models.CharField(
        max_length=255,
        help_text="URL (https://...) or static path (example: blog/assets/img/certificate.jpg).",
    )
    certificate_source = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL or static path to the certificate/document.",
    )
    cta_label = models.CharField(max_length=80, default="Open certificate")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def _resolve_source(self, value):
        if not value:
            return ""
        if value.startswith(("http://", "https://", "/")):
            return value
        return static(value)

    @property
    def image_url(self):
        return self._resolve_source(self.image_source)

    @property
    def certificate_url(self):
        return self._resolve_source(self.certificate_source or self.image_source)


class DiplomaCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140] or "diploma-category"
        super().save(*args, **kwargs)


class ProjectItem(models.Model):
    class Category(models.TextChoices):
        LIVE = "live", "Projet live"
        PROJECT = "project", "Projet"

    category = models.CharField(max_length=20, choices=Category.choices, default=Category.PROJECT)
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    cover_source = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL (https://...) or static path (example: blog/assets/img/project-cover.jpg).",
    )
    live_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="External URL (https://...) or internal path (example: /projects/weather-live/).",
    )
    source_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:220] or "project-item"
            slug = base_slug
            counter = 2
            while ProjectItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug[:220-len(str(counter))-1]}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def _resolve_source(self, value):
        if not value:
            return ""
        if value.startswith(("http://", "https://", "/")):
            return value
        return static(value)

    @property
    def cover_url(self):
        return self._resolve_source(self.cover_source)


def normalize_youtube_url(url):
    if not url:
        return url
    iframe_match = re.search(r'src="([^"]+)"', url)
    if iframe_match:
        url = iframe_match.group(1)
    parsed = urlparse(url)
    if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        if parsed.path.startswith("/embed/"):
            return url
        query = parse_qs(parsed.query)
        video_id = query.get("v", [None])[0]
        if video_id:
            start = query.get("t", [None])[0] or query.get("start", [None])[0]
            start_seconds = 0
            if start:
                if isinstance(start, str) and start.endswith("s"):
                    start = start[:-1]
                if start.isdigit():
                    start_seconds = int(start)
            embed = f"https://www.youtube.com/embed/{video_id}"
            if start_seconds:
                embed += f"?start={start_seconds}"
            return embed
    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.lstrip("/")
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    return url


class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_progress")
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, related_name="progress_entries")
    is_watched = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")
        ordering = ["-updated_at"]

    def __str__(self):
        status = "watched" if self.is_watched else "in progress"
        return f"{self.user} - {self.video.title} ({status})"


class CourseComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_comments")
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} - {self.video.title}"


class CourseCommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_comment_likes")
    comment = models.ForeignKey(CourseComment, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.comment_id}"
