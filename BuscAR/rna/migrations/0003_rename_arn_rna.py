# Generated by Django 4.2.1 on 2023-07-06 01:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rna', '0002_alter_arn_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ARN',
            new_name='RNA',
        ),
    ]