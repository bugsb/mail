# Generated by Django 3.2 on 2021-05-06 08:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_mail_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail_detail',
            name='file',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
