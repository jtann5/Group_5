# Generated by Django 5.0.2 on 2024-02-17 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0006_alter_useraccount_managers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="username",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]