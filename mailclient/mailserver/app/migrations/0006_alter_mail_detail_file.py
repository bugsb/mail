# Generated by Django 3.2 on 2021-05-07 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_mail_detail_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail_detail',
            name='file',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
