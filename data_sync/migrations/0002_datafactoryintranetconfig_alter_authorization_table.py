# Generated by Django 4.1.3 on 2023-04-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_sync', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFactoryIntranetConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('host', models.GenericIPAddressField()),
                ('port', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=1000)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('u_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 't_intranet_config',
            },
        ),
        migrations.AlterModelTable(
            name='authorization',
            table='t_auth',
        ),
    ]
