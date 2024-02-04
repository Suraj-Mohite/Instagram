# Generated by Django 5.0.1 on 2024-02-04 13:12

import django.db.models.deletion
import post.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0007_alter_post_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stream",
            options={"ordering": ["-date"]},
        ),
        migrations.CreateModel(
            name="PostImage",
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
                (
                    "image",
                    models.ImageField(
                        null=True,
                        upload_to=post.utils.get_user_directory_path,
                        verbose_name="Picture",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_images",
                        to="post.post",
                    ),
                ),
            ],
        ),
    ]