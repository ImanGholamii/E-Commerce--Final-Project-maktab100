# Generated by Django 4.2.7 on 2024-01-30 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_otpcode_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('manager', 'Manager'), ('operator', 'Operator'), ('viewer', 'Viewer')], max_length=100, verbose_name='Role'),
        ),
    ]
