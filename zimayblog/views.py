from django.contrib import messages
from django.shortcuts import redirect, render

from app.content import POSTS
from app.models import ContactLead


def home(request):
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
                "Your request has been received. Moses can now review it and follow up.",
            )
            return redirect("/#contact")

        messages.error(
            request,
            "Please complete your name, email and project message before sending.",
        )

    services = [
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
    ]

    strengths = [
        "Accounting Assistant experience at the Inter-African Coffee Organization",
        "Hands-on multi-currency finance management across XOF and EUR",
        "Operational knowledge of SAGE, QuickBooks and Xero",
        "Experience supporting NGOs and international organizations",
        "A rare blend of finance rigor, web delivery and digital security mindset",
        "Bilingual business communication for Francophone and Anglophone audiences",
    ]

    metrics = [
        {"value": "Finance + Digital", "label": "One partner for compliance, websites and growth"},
        {"value": "NGO Ready", "label": "Strong fit for donor-facing and international environments"},
        {"value": "OHADA Aligned", "label": "Reporting and structuring built for West and Central Africa"},
        {"value": "24/7 Mindset", "label": "Fast response for urgent business and digital issues"},
    ]

    testimonials = [
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
    ]

    pricing = [
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
    ]

    credentials = [
        {
            "title": "Wealth Management, Private Banking & Compliance Introduction",
            "issuer": "Udemy / MTF Institute of Management, Technology and Finance",
            "date": "26 March 2026",
            "summary": "A recent certification reinforcing Moses Zegbah Zimay's positioning around compliance, financial standards and trusted advisory.",
            "image": "blog/assets/img/wealth-management-certificate.jpeg",
            "link": "blog/assets/img/wealth-management-certificate.jpeg",
            "cta": "Open certificate",
        }
    ]

    featured_video = {
        "title": "Featured YouTube video",
        "summary": "Replace this placeholder with one of your YouTube video links. The hover preview is already ready in the header.",
        "url": "https://youtu.be/3v2hf2maqvQ?si=zT1at2Wvy55ZROB6",
        "label": "Video preview",
        "placeholder": True,
    }

    context = {
        "services": services,
        "strengths": strengths,
        "metrics": metrics,
        "testimonials": testimonials,
        "pricing": pricing,
        "posts": POSTS,
        "credentials": credentials,
        "featured_video": featured_video,
        "portfolio_url": "https://zimaymoseszegbah-portofolio.netlify.app/",
        "cv_url": "blog/assets/docs/moses-zegbah-zimay-cv.pdf",
    }
    return render(request, "home.html", context)


def about(request):
    return redirect("/#about")


def project(request):
    return redirect("/#services")


def gallery(request):
    return redirect("/#results")


def contact(request):
    return redirect("/#contact")
