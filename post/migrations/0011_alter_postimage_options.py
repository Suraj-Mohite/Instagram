# Generated by Django 5.0.1 on 2024-02-04 14:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0010_rename_tag_post_tags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postimage",
            options={"ordering": ["-id"]},
        ),
    ]
