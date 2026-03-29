from django.db import migrations


def add_todo_project(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.update_or_create(
        slug="todo-list-live",
        defaults={
            "category": "live",
            "title": "Todo List App",
            "summary": "Todo app avec ajout, suppression et validation des taches.",
            "description": "Version live integree depuis vos fichiers Flask (HTML/CSS/JS), avec stockage local navigateur.",
            "live_url": "/projects/todo-live/",
            "source_url": "",
            "is_published": True,
            "order": 3,
        },
    )


def remove_todo_project(apps, schema_editor):
    ProjectItem = apps.get_model("blog", "ProjectItem")
    ProjectItem.objects.filter(slug="todo-list-live").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_seed_projects"),
    ]

    operations = [
        migrations.RunPython(add_todo_project, remove_todo_project),
    ]
