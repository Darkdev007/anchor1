# Generated by Django 3.2.7 on 2021-09-29 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anchorapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'managed': True, 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
    ]
