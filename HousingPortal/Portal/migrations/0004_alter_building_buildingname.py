# Generated by Django 5.0.2 on 2024-02-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0003_building_buildingname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="building",
            name="buildingName",
            field=models.CharField(default="", max_length=100),
        ),
    ]