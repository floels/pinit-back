# Generated by Django 4.2.5 on 2023-11-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinit_api', '0014_alter_pin_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
