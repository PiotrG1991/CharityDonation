# Generated by Django 5.0.3 on 2024-03-26 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CharityAPP', '0003_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
