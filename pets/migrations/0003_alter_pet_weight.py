# Generated by Django 4.2.2 on 2023-06-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_pet_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="weight",
            field=models.FloatField(),
        ),
    ]
