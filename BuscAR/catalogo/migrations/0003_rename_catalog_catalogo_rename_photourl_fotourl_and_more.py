# Generated by Django 4.2.1 on 2023-07-06 01:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogo', '0002_rename_catalogo_photourl_objeto'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catalog',
            new_name='Catalogo',
        ),
        migrations.RenameModel(
            old_name='PhotoUrl',
            new_name='fotoUrl',
        ),
        migrations.RenameModel(
            old_name='MyObject',
            new_name='Objeto',
        ),
    ]
