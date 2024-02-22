# Generated by Django 4.2.7 on 2024-01-22 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customer_created_at_customer_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Profile Picture'),
        ),
    ]
