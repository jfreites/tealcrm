# Generated by Django 4.2.3 on 2023-07-16 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('name',)},
        ),
    ]
