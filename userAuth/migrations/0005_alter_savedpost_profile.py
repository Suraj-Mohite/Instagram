# Generated by Django 5.0.1 on 2024-02-10 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userAuth", "0004_alter_savedpost_post_alter_savedpost_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savedpost",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile_saved",
                to="userAuth.profile",
            ),
        ),
    ]