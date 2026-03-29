from django.db import migrations


def update_project_copy_and_previews(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")

    ProjectItem.objects.filter(slug="skycast-pro-meteo-live").update(
        cover_source="blog/assets/img/projects/skycast-preview.svg",
        summary="Application meteo avec recherche rapide par ville.",
        description="Affichage de la temperature, de l'humidite et du vent dans une interface claire.",
    )

    ProjectItem.objects.filter(slug="plateforme-cours-blog-participatif").update(
        cover_source="blog/assets/img/projects/platform-preview.svg",
        summary="Plateforme principale avec cours structures et blog participatif.",
        description="Inclut espace cours, progression, commentaires et validation admin.",
    )

    ProjectItem.objects.filter(slug="todo-list-live").update(
        cover_source="blog/assets/img/projects/todo-preview.svg",
        summary="Todo app avec ajout, suppression et validation des taches.",
        description="Interface simple pour organiser les taches quotidiennes.",
    )


def rollback_project_copy_and_previews(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")

    ProjectItem.objects.filter(slug="skycast-pro-meteo-live").update(
        cover_source="",
        summary="Application meteo issue de vos fichiers HTML/CSS/JS.",
        description="Recherche d'une ville, affichage temperature/humidite/vent, et rendu mobile-friendly.",
    )

    ProjectItem.objects.filter(slug="plateforme-cours-blog-participatif").update(
        cover_source="",
        summary="Projet principal du site avec cours, progression et contributions utilisateurs.",
        description="Inclut espace cours, commentaires, diplomes, blog participatif et validation admin.",
    )

    ProjectItem.objects.filter(slug="todo-list-live").update(
        cover_source="",
        summary="Todo app avec ajout, suppression et validation des taches.",
        description="Version live integree depuis vos fichiers Flask (HTML/CSS/JS), avec stockage local navigateur.",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_add_nadrelie_project"),
    ]

    operations = [
        migrations.RunPython(update_project_copy_and_previews, rollback_project_copy_and_previews),
    ]
