# Generated by Django 4.2.7 on 2023-11-12 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0018_alter_tasks_submittime"),
    ]

    operations = [
        migrations.AddField(
            model_name="tasks",
            name="fileID",
            field=models.CharField(
                default="1", max_length=64, primary_key=True, serialize=False
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="tasks",
            name="taskID",
            field=models.CharField(max_length=64),
        ),
    ]
