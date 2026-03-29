from django.db import migrations


def add_nadrelie_project(apps, schema_editor):
    ProjectItem = apps.get_model("app", "ProjectItem")
    ProjectItem.objects.update_or_create(
        slug="nadrelie-site-live",
        defaults={
            "category": "live",
            "title": "Nadrelie Website",
            "summary": "Site vitrine ajoute dans la section projets live.",
            "description": "Previsualisation disponible sur la carte projet et acces direct au site public.",
            "cover_source": "https://s.wordpress.com/mshots/v1/https%3A%2F%2Fnadrelie.com%2F?w=1200",
            "live_url": "https://nadrelie.com/",
            "source_url": "",
            "is_published": True,
            "order": 4,
        },
    )


def remove_nadrelie_project(apps, schema_editor):
    ProjectItem = apps.get_model("app", "ProjectItem")
    ProjectItem.objects.filter(slug="nadrelie-site-live").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_add_todo_project"),
    ]

    operations = [
        migrations.RunPython(add_nadrelie_project, remove_nadrelie_project),
    ]
