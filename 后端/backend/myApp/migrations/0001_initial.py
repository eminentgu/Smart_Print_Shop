# Generated by Django 4.2.7 on 2023-11-10 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "userID",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("username", models.CharField(max_length=64)),
                ("password", models.CharField(max_length=64)),
            ],
        ),
    ]
