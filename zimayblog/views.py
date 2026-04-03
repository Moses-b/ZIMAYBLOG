from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from urllib.parse import parse_qs, urlparse

from app.models import (
    ContactLead,
    CourseCategory,
    CourseComment,
    CourseCommentLike,
    CourseProgress,
    CourseVideo,
    DiplomaCategory,
    Diploma,
    ProjectItem,
    normalize_youtube_url,
)
from app.services import get_public_posts
from .forms import SignupForm
from .localization import (
    DEFAULT_LANGUAGE,
    SESSION_LANGUAGE_KEY,
    SUPPORTED_LANGUAGES,
    get_home_content,
    get_language,
    get_ui_text,
)


def _featured_video_for_language(language):
    featured_video_by_language = {
        "en": {
            "title": "Free Courses Library",
            "summary": "Access curated courses by category after login.",
            "url": "/courses/",
            "label": "Free Courses",
            "placeholder": False,
        },
        "fr": {
            "title": "Bibliotheque de cours gratuits",
            "summary": "Accedez aux cours par categorie apres connexion.",
            "url": "/courses/",
            "label": "Cours Gratuits",
            "placeholder": False,
        },
    }
    return featured_video_by_language.get(language, featured_video_by_language["en"])


def _serialize_diploma(diploma):
    return {
        "category": diploma.category.name if diploma.category else "",
        "title": diploma.title,
        "issuer": diploma.issuer,
        "date": diploma.date_label,
        "summary": diploma.summary,
        "image_url": diploma.image_url,
        "link_url": diploma.certificate_url,
        "cta": diploma.cta_label,
    }


def home(request):
    language = get_language(request)
    ui = get_ui_text(language)
    copy = get_home_content(language)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        service = request.POST.get("service", "").strip()
        message = request.POST.get("message", "").strip()

        if name and email and message:
            ContactLead.objects.create(
                name=name,
                email=email,
                service=service,
                message=message,
            )
            messages.success(
                request,
                ui["success_message"],
            )
            return redirect("/#contact")

        messages.error(
            request,
            ui["error_message"],
        )

    services_by_language = {
        "en": [
            {
                "eyebrow": "WordPress & Shopify",
                "title": "Conversion-focused website creation",
                "description": "Premium showcase sites, business websites and e-commerce stores designed to convert, rank and inspire trust.",
                "price": "From 300,000 FCFA",
            },
            {
                "eyebrow": "Protection & Monitoring",
                "title": "Maintenance and digital security",
                "description": "Monthly care plans, uptime monitoring, backup strategy, plugin hygiene and protection against common attacks.",
                "price": "From 75,000 FCFA / month",
            },
            {
                "eyebrow": "OHADA / SYCEBNL / IFRS",
                "title": "Accounting and compliance advisory",
                "description": "Bookkeeping, chart of accounts, financial statements, reconciliations, budget tracking and audit preparation.",
                "price": "Custom engagement",
            },
            {
                "eyebrow": "Growth & Structuring",
                "title": "Business and e-commerce consulting",
                "description": "Support for company setup, international business structuring, e-commerce expansion and financial visibility.",
                "price": "Strategy sessions available",
            },
        ],
        "fr": [
            {
                "eyebrow": "WordPress et Shopify",
                "title": "Creation de sites web orientee conversion",
                "description": "Sites vitrine premium, sites d'entreprise et boutiques e-commerce pensés pour convertir, bien se positionner et inspirer confiance.",
                "price": "A partir de 300 000 FCFA",
            },
            {
                "eyebrow": "Protection et suivi",
                "title": "Maintenance et securite numerique",
                "description": "Plans mensuels, surveillance de disponibilite, strategie de sauvegarde, hygiene des plugins et protection contre les attaques courantes.",
                "price": "A partir de 75 000 FCFA / mois",
            },
            {
                "eyebrow": "OHADA / SYCEBNL / IFRS",
                "title": "Conseil comptable et conformite",
                "description": "Tenue comptable, plan de comptes, etats financiers, rapprochements, suivi budgetaire et preparation a l'audit.",
                "price": "Mission sur mesure",
            },
            {
                "eyebrow": "Croissance et structuration",
                "title": "Conseil business et e-commerce",
                "description": "Appui a la creation d'entreprise, structuration internationale, expansion e-commerce et visibilite financiere.",
                "price": "Sessions strategie disponibles",
            },
        ],
    }

    services = services_by_language[language]

    strengths_by_language = {
        "en": [
            "Accounting Assistant experience at the Inter-African Coffee Organization",
            "Hands-on multi-currency finance management across XOF and EUR",
            "Operational knowledge of SAGE, QuickBooks and Xero",
            "Experience supporting NGOs and international organizations",
            "A rare blend of finance rigor, web delivery and digital security mindset",
            "Bilingual business communication for Francophone and Anglophone audiences",
        ],
        "fr": [
            "Experience d'assistant comptable a l'Organisation Interafricaine du Cafe",
            "Pratique de la gestion financiere multi-devises en XOF et EUR",
            "Maitrise operationnelle de SAGE, QuickBooks et Xero",
            "Experience d'appui aux ONG et aux organisations internationales",
            "Un melange rare entre rigueur financiere, delivery web et culture securite numerique",
            "Communication business bilingue pour des publics francophones et anglophones",
        ],
    }

    strengths = strengths_by_language[language]

    metrics_by_language = {
        "en": [
            {"value": "Finance + Digital", "label": "One partner for compliance, websites and growth"},
            {"value": "NGO Ready", "label": "Strong fit for donor-facing and international environments"},
            {"value": "OHADA Aligned", "label": "Reporting and structuring built for West and Central Africa"},
            {"value": "24/7 Mindset", "label": "Fast response for urgent business and digital issues"},
        ],
        "fr": [
            {"value": "Finance + Digital", "label": "Un seul partenaire pour la conformite, les sites web et la croissance"},
            {"value": "Pret pour les ONG", "label": "Un profil adapte aux environnements bailleurs et internationaux"},
            {"value": "Aligne OHADA", "label": "Reporting et structuration pensés pour l'Afrique de l'Ouest et centrale"},
            {"value": "Mentalite 24/7", "label": "Reponse rapide pour les urgences business et digitales"},
        ],
    }

    metrics = metrics_by_language[language]

    testimonials_by_language = {
        "en": [
            {
                "quote": "Moses combines accounting discipline with digital execution. We did not just get a website, we gained a more credible business system.",
                "name": "SME Founder",
                "role": "Retail and Distribution, Abidjan",
            },
            {
                "quote": "His understanding of reconciliations, reporting and operational controls made our finance process more reliable and audit-ready.",
                "name": "Program Operations Lead",
                "role": "NGO Partner",
            },
            {
                "quote": "The rare value is the double expertise. He speaks finance like an accountant and growth like a digital consultant.",
                "name": "E-commerce Entrepreneur",
                "role": "Cross-border Seller",
            },
        ],
        "fr": [
            {
                "quote": "Moses combine la discipline comptable avec l'execution digitale. Nous n'avons pas seulement obtenu un site web, nous avons gagne un systeme d'entreprise plus credible.",
                "name": "Fondateur de PME",
                "role": "Retail et distribution, Abidjan",
            },
            {
                "quote": "Sa maitrise des rapprochements, du reporting et des controles operationnels a rendu notre processus finance plus fiable et pret pour l'audit.",
                "name": "Responsable operations programme",
                "role": "Partenaire ONG",
            },
            {
                "quote": "La vraie rarete, c'est la double expertise. Il parle finance comme un comptable et croissance comme un consultant digital.",
                "name": "Entrepreneur e-commerce",
                "role": "Vente transfrontaliere",
            },
        ],
    }

    testimonials = testimonials_by_language[language]

    pricing_by_language = {
        "en": [
            {
                "name": "Website Launch",
                "price": "300,000 FCFA+",
                "description": "For businesses that need a credible digital presence with strong messaging and conversion structure.",
                "features": [
                    "WordPress or Shopify build",
                    "Premium landing pages",
                    "Mobile-first UX",
                    "On-page SEO foundation",
                ],
            },
            {
                "name": "Security and Maintenance",
                "price": "75,000 FCFA / month+",
                "description": "For founders who want peace of mind, stable performance and ongoing protection.",
                "features": [
                    "Core and plugin updates",
                    "Backup and monitoring",
                    "Security checks",
                    "Monthly support window",
                ],
            },
            {
                "name": "Advisory Premium",
                "price": "Custom retainer",
                "description": "For SMEs, NGOs and fast-moving teams that need finance, compliance and growth support together.",
                "features": [
                    "Accounting and compliance advisory",
                    "Financial structuring",
                    "Business coaching",
                    "Priority consulting access",
                ],
            },
        ],
        "fr": [
            {
                "name": "Lancement de site web",
                "price": "300 000 FCFA+",
                "description": "Pour les entreprises qui ont besoin d'une presence digitale credible avec un message fort et une structure de conversion solide.",
                "features": [
                    "Creation WordPress ou Shopify",
                    "Landing pages premium",
                    "UX mobile-first",
                    "Base SEO on-page",
                ],
            },
            {
                "name": "Securite et maintenance",
                "price": "75 000 FCFA / mois+",
                "description": "Pour les fondateurs qui veulent de la serenite, une performance stable et une protection continue.",
                "features": [
                    "Mises a jour coeur et plugins",
                    "Sauvegarde et monitoring",
                    "Verifications securite",
                    "Support mensuel",
                ],
            },
            {
                "name": "Conseil premium",
                "price": "Retainer sur mesure",
                "description": "Pour les PME, ONG et equipes agiles qui ont besoin d'un accompagnement combine en finance, conformite et croissance.",
                "features": [
                    "Conseil comptable et conformite",
                    "Structuration financiere",
                    "Coaching business",
                    "Acces prioritaire au conseil",
                ],
            },
        ],
    }

    pricing = pricing_by_language[language]
    latest_diploma = Diploma.objects.filter(is_published=True).first()
    if latest_diploma:
        credentials = [_serialize_diploma(latest_diploma)]
    else:
        credentials = [
            {
                "title": "Wealth Management, Private Banking & Compliance Introduction"
                if language == "en"
                else "Introduction a la gestion de patrimoine, a la banque privee et a la conformite",
                "issuer": "Udemy / MTF Institute of Management, Technology and Finance",
                "date": "26 March 2026" if language == "en" else "26 mars 2026",
                "summary": "A recent certification reinforcing Moses Zegbah Zimay's positioning around compliance, financial standards and trusted advisory."
                if language == "en"
                else "Une certification recente qui renforce le positionnement de Moses Zegbah Zimay autour de la conformite, des standards financiers et du conseil de confiance.",
                "image_url": "/static/blog/assets/img/wealth-management-certificate.jpeg",
                "link_url": "/static/blog/assets/img/wealth-management-certificate.jpeg",
                "cta": "Open certificate" if language == "en" else "Ouvrir le certificat",
            }
        ]

    featured_video = _featured_video_for_language(language)

    context = {
        "services": services,
        "strengths": strengths,
        "metrics": metrics,
        "testimonials": testimonials,
        "pricing": pricing,
        "posts": get_public_posts(language)[:4],
        "credentials": credentials,
        "featured_video": featured_video,
        "portfolio_url": "https://www.tiktok.com/@zacofficiel225",
        "cv_url": "blog/assets/docs/moses-zegbah-zimay-cv.pdf",
        "ui": ui,
        "copy": copy,
        "current_language": language,
    }
    return render(request, "home.html", context)


def about(request):
    return redirect("/#about")


def project(request):
    return redirect("/projects/")


def gallery(request):
    return redirect("/#results")


def contact(request):
    return redirect("/#contact")


def _serialize_project(item, ui):
    is_live = item.category == ProjectItem.Category.LIVE
    return {
        "title": item.title,
        "slug": item.slug,
        "summary": item.summary,
        "description": item.description,
        "category": item.category,
        "category_label": ui["projects_live_badge"] if is_live else ui["projects_build_badge"],
        "cover_url": item.cover_url,
        "live_url": item.live_url,
        "source_url": item.source_url,
    }


def projects(request):
    language = get_language(request)
    ui = get_ui_text(language)
    selected_type = request.GET.get("type", "").strip()
    valid_types = {ProjectItem.Category.LIVE, ProjectItem.Category.PROJECT}

    queryset = ProjectItem.objects.filter(is_published=True)
    if selected_type in valid_types:
        queryset = queryset.filter(category=selected_type)
    else:
        selected_type = ""

    all_items = list(ProjectItem.objects.filter(is_published=True))
    live_count = len([item for item in all_items if item.category == ProjectItem.Category.LIVE])
    project_count = len([item for item in all_items if item.category == ProjectItem.Category.PROJECT])
    projects_payload = [_serialize_project(item, ui) for item in queryset]

    return render(
        request,
        "projects/list.html",
        {
            "ui": ui,
            "current_language": language,
            "featured_video": _featured_video_for_language(language),
            "projects": projects_payload,
            "selected_project_type": selected_type,
            "live_count": live_count,
            "project_count": project_count,
        },
    )


def weather_project_live(request):
    language = get_language(request)
    return render(
        request,
        "projects/weather_live.html",
        {
            "ui": get_ui_text(language),
            "current_language": language,
            "featured_video": _featured_video_for_language(language),
        },
    )


def todo_project_live(request):
    language = get_language(request)
    return render(
        request,
        "projects/todo_live.html",
        {
            "ui": get_ui_text(language),
            "current_language": language,
            "featured_video": _featured_video_for_language(language),
        },
    )


def diplomas(request):
    language = get_language(request)
    ui = get_ui_text(language)
    category_slug = request.GET.get("category", "").strip()
    categories = list(DiplomaCategory.objects.all())
    queryset = Diploma.objects.filter(is_published=True).select_related("category")
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    items = [_serialize_diploma(item) for item in queryset]
    return render(
        request,
        "diplomas.html",
        {
            "ui": ui,
            "current_language": language,
            "diplomas": items,
            "diploma_categories": categories,
            "selected_diploma_category": category_slug,
            "featured_video": _featured_video_for_language(language),
        },
    )


def set_language(request):
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if request.method == "POST":
        language = request.POST.get("language", DEFAULT_LANGUAGE)
        if language in SUPPORTED_LANGUAGES:
            request.session[SESSION_LANGUAGE_KEY] = language
    return redirect(next_url)


class UserLoginView(LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = get_language(self.request)
        context.update(
            {
                "ui": get_ui_text(language),
                "current_language": language,
                "tiktok_url": "https://www.tiktok.com/@zacofficiel225",
            }
        )
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        language = get_language(self.request)
        ui = get_ui_text(language)
        messages.success(self.request, ui["login_success"])
        return response


def signup(request):
    language = get_language(request)
    ui = get_ui_text(language)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_path = f"/accounts/activate/{uid}/{token}/"
            activation_link = request.build_absolute_uri(activate_path)
            email_body = render_to_string(
                "registration/activation_email.txt",
                {"user": user, "activation_link": activation_link},
            )
            send_mail(
                subject="Activate your account",
                message=email_body,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            messages.success(
                request,
                ui["signup_success"],
            )
            return redirect("/accounts/login/")
    else:
        form = SignupForm()
    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
            "ui": ui,
            "current_language": language,
            "tiktok_url": "https://www.tiktok.com/@zacofficiel225",
        },
    )


def activate_account(request, uidb64, token):
    language = get_language(request)
    ui = get_ui_text(language)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, ui["activation_success"])
        return redirect("/accounts/login/")

    return HttpResponse("Invalid activation link.", status=400)


@login_required
def courses(request):
    language = get_language(request)
    ui = get_ui_text(language)
    categories = CourseCategory.objects.prefetch_related("subcategories").all()
    videos = CourseVideo.objects.filter(is_published=True).select_related("category", "subcategory")
    def extract_video_id(url):
        url = normalize_youtube_url(url)
        parsed = urlparse(url)
        if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com") and parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[-1]
        if parsed.hostname in ("youtu.be", "www.youtu.be"):
            return parsed.path.lstrip("/")
        if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
            query = parse_qs(parsed.query)
            return query.get("v", [None])[0]
        return None

    def to_embed(url):
        # Accept raw iframe strings and legacy watch/short links.
        url = normalize_youtube_url(url)
        parsed = urlparse(url)
        if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com") and parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/")[-1]
            query = parse_qs(parsed.query)
            start = query.get("t", [None])[0] or query.get("start", [None])[0]
            start_seconds = 0
            if start:
                if isinstance(start, str) and start.endswith("s"):
                    start = start[:-1]
                if start.isdigit():
                    start_seconds = int(start)
            embed = f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&autoplay=1&mute=1&rel=0"
            if start_seconds:
                embed += f"&start={start_seconds}"
            return embed
        query = parse_qs(parsed.query)
        start = query.get("t", [None])[0] or query.get("start", [None])[0]
        start_seconds = 0
        if start:
            if isinstance(start, str) and start.endswith("s"):
                start = start[:-1]
            if start.isdigit():
                start_seconds = int(start)
        if parsed.hostname in ("youtu.be", "www.youtu.be"):
            embed = f"https://www.youtube.com/embed/{parsed.path.lstrip('/')}?enablejsapi=1&autoplay=1&mute=1&rel=0"
            if start_seconds:
                embed += f"&start={start_seconds}"
            return embed
        if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
            video_id = query.get("v", [None])[0]
            if video_id:
                embed = f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&autoplay=1&mute=1&rel=0"
                if start_seconds:
                    embed += f"&start={start_seconds}"
                return embed
        return url

    if request.method == "POST":
        action = request.POST.get("action")
        video_id = request.POST.get("video_id")
        next_url = request.POST.get("next") or "/courses/"
        if action == "toggle_watched" and video_id:
            progress, _ = CourseProgress.objects.get_or_create(user=request.user, video_id=video_id)
            progress.is_watched = not progress.is_watched
            progress.save()
            return redirect(next_url)
        if action == "mark_watched" and video_id:
            progress, _ = CourseProgress.objects.get_or_create(user=request.user, video_id=video_id)
            if not progress.is_watched:
                progress.is_watched = True
                progress.save()
            return redirect(next_url)
        if action == "comment" and video_id:
            content = request.POST.get("content", "").strip()
            if content:
                CourseComment.objects.create(user=request.user, video_id=video_id, content=content)
            return redirect(next_url)
        if action == "toggle_like":
            comment_id = request.POST.get("comment_id")
            if comment_id:
                like, created = CourseCommentLike.objects.get_or_create(user=request.user, comment_id=comment_id)
                if not created:
                    like.delete()
            return redirect(next_url)

    watched_ids = set(
        CourseProgress.objects.filter(user=request.user, is_watched=True).values_list("video_id", flat=True)
    )

    selected_video_id = request.GET.get("video")
    selected_video = None
    if selected_video_id:
        selected_video = videos.filter(id=selected_video_id).first()
    if not selected_video:
        selected_video = videos.order_by("order", "-created_at").first()
    selected_category_id = selected_video.category_id if selected_video else None
    if selected_video:
        selected_video.embed_url = to_embed(selected_video.youtube_url)
        selected_id = extract_video_id(selected_video.youtube_url)
        if selected_id:
            selected_video.watch_url = f"https://www.youtube.com/watch?v={selected_id}"
        else:
            selected_video.watch_url = selected_video.youtube_url

    video_list = list(videos.order_by("order", "-created_at"))
    category_map = {}
    for category in categories:
        category_map[category.id] = {
            "category": category,
            "videos": [],
            "subcategories": {sub.id: {"subcategory": sub, "videos": []} for sub in category.subcategories.all()},
        }
    for video in video_list:
        video.embed_url = to_embed(video.youtube_url)
        video_id = extract_video_id(video.youtube_url)
        if video_id:
            video.thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            video.watch_url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            video.watch_url = video.youtube_url
        entry = category_map.get(video.category_id)
        if not entry:
            continue
        if video.subcategory_id and video.subcategory_id in entry["subcategories"]:
            entry["subcategories"][video.subcategory_id]["videos"].append(video)
        else:
            entry["videos"].append(video)

    categories_data = []
    for entry in category_map.values():
        all_videos = entry["videos"][:]
        for sub in entry["subcategories"].values():
            all_videos.extend(sub["videos"])
        total_count = len(all_videos)
        watched_count = len([video for video in all_videos if video.id in watched_ids])
        progress_pct = int((watched_count / total_count) * 100) if total_count else 0
        categories_data.append(
            {
                "category": entry["category"],
                "videos": entry["videos"],
                "subcategories": entry["subcategories"],
                "total_count": total_count,
                "watched_count": watched_count,
                "progress_pct": progress_pct,
            }
        )

    comments = []
    if selected_video:
        comments = (
            CourseComment.objects.filter(video=selected_video)
            .select_related("user")
            .prefetch_related("likes")
        )

    liked_comment_ids = set(
        CourseCommentLike.objects.filter(user=request.user, comment__video=selected_video)
        .values_list("comment_id", flat=True)
    ) if selected_video else set()

    context = {
        "ui": ui,
        "current_language": language,
        "tiktok_url": "https://www.tiktok.com/@zacofficiel225",
        "categories": categories_data,
        "selected_video": selected_video,
        "selected_category_id": selected_category_id,
        "comments": comments,
        "watched_ids": watched_ids,
        "liked_comment_ids": liked_comment_ids,
    }
    return render(request, "courses.html", context)
