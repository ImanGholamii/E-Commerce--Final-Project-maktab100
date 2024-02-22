# Generated by Django 4.2.7 on 2024-01-22 09:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_userprofile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Created at this time', verbose_name='Created time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Modified at this time', verbose_name='Modified time'),
        ),
        migrations.AddField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Created at this time', verbose_name='Created time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Modified at this time', verbose_name='Modified time'),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Created at this time', verbose_name='Created time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Modified at this time', verbose_name='Modified time'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Created at this time', verbose_name='Created time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Modified at this time', verbose_name='Modified time'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='addresses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='users.address', verbose_name='Address'),
        ),
    ]
