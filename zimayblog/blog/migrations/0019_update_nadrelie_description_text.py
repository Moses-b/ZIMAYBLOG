from django.db import migrations


def update_nadrelie_description_text(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(slug="nadrelie-site-live").update(
        summary=(
            "Nadrélie est une marque ivoirienne de soins cosmétiques et "
            "thérapeutiques \"ancestraux\", fondée par Casthelie Légré. "
            "Basée à Abidjan, elle se spécialise dans des produits naturels "
            "inspirés des traditions et des habitudes culinaires africaines."
        ),
        description="",
    )


def rollback_nadrelie_description_text(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(slug="nadrelie-site-live").update(
        summary="Nadrelie est un site professionnel moderne qui presente clairement la marque, les services et les points de contact.",
        description="",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0018_update_nadrelie_description"),
    ]

    operations = [
        migrations.RunPython(update_nadrelie_description_text, rollback_nadrelie_description_text),
    ]
