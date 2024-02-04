# Generated by Django 5.0.1 on 2024-01-25 20:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0005_alter_post_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tag",
            field=models.ManyToManyField(
                blank=True, related_name="tags", to="post.tag"
            ),
        ),
    ]