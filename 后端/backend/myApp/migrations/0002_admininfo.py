# Generated by Django 4.2.7 on 2023-11-10 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminInfo",
            fields=[
                (
                    "adminID",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("adminname", models.CharField(max_length=64)),
                ("password", models.CharField(max_length=64)),
            ],
        ),
    ]
