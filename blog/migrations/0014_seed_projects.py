from django.db import migrations


def seed_projects(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")

    defaults = [
        {
            "category": "live",
            "title": "SkyCast Pro - Meteo en direct",
            "slug": "skycast-pro-meteo-live",
            "summary": "Application meteo issue de vos fichiers HTML/CSS/JS.",
            "description": "Recherche d'une ville, affichage temperature/humidite/vent, et rendu mobile-friendly.",
            "live_url": "/projects/weather-live/",
            "source_url": "",
            "is_published": True,
            "order": 1,
        },
        {
            "category": "project",
            "title": "Plateforme cours + blog participatif",
            "slug": "plateforme-cours-blog-participatif",
            "summary": "Projet principal du site avec cours, progression et contributions utilisateurs.",
            "description": "Inclut espace cours, commentaires, diplomes, blog participatif et validation admin.",
            "live_url": "/",
            "source_url": "",
            "is_published": True,
            "order": 2,
        },
    ]

    for item in defaults:
        ProjectItem.objects.update_or_create(slug=item["slug"], defaults=item)


def unseed_projects(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(
        slug__in=["skycast-pro-meteo-live", "plateforme-cours-blog-participatif"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_projectitem"),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
    ]
