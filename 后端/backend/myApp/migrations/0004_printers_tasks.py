# Generated by Django 4.2.7 on 2023-11-10 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0003_alter_admininfo_adminname_alter_userinfo_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="Printers",
            fields=[
                (
                    "printerID",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("printerName", models.CharField(max_length=64)),
                ("paperVol", models.IntegerField()),
                ("inkVol", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Tasks",
            fields=[
                (
                    "taskID",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("userID", models.CharField(max_length=64)),
                ("printerID", models.CharField(max_length=64)),
                ("taskStatus", models.CharField(max_length=64)),
            ],
        ),
    ]
