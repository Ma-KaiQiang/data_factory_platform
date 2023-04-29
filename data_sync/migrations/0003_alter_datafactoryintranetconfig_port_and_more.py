# Generated by Django 4.1.3 on 2023-04-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_sync', '0002_datafactoryintranetconfig_alter_authorization_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafactoryintranetconfig',
            name='port',
            field=models.CharField(default=3306, max_length=10),
        ),
        migrations.AlterField(
            model_name='datafactoryintranetconfig',
            name='remark',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
