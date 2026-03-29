from django.db import migrations


def update_nadrelie_description(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(slug="nadrelie-site-live").update(
        summary="Nadrelie est un site professionnel moderne qui presente clairement la marque, les services et les points de contact.",
        description="",
    )


def rollback_nadrelie_description(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(slug="nadrelie-site-live").update(
        summary="Site vitrine ajoute dans la section projets live.",
        description="Previsualisation disponible sur la carte projet et acces direct au site public.",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0017_update_project_copy_and_previews"),
    ]

    operations = [
        migrations.RunPython(update_nadrelie_description, rollback_nadrelie_description),
    ]
