# Generated by Django 5.0.1 on 2024-02-10 07:48

import base.utils
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("post", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("first_name", models.CharField(blank=True, max_length=150, null=True)),
                ("last_name", models.CharField(blank=True, max_length=150, null=True)),
                ("location", models.CharField(blank=True, max_length=150, null=True)),
                ("bio", models.CharField(blank=True, max_length=300, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        default="default.jpg",
                        upload_to=base.utils.get_user_directory_path,
                    ),
                ),
                (
                    "favourite",
                    models.ManyToManyField(related_name="favourite", to="post.post"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
