# Generated by Django 4.2.2 on 2024-07-22 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
