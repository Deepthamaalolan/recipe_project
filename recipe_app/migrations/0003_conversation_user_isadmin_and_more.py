# Generated by Django 4.1.13 on 2023-12-05 14:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe_app", "0002_recipe_user_favorites_alter_user_userid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("messages", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="isadmin",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="dietary_preferences",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="favorites",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="meal_preferences",
            field=models.CharField(max_length=255),
        ),
    ]