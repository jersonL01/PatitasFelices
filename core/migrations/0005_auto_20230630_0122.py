# Generated by Django 3.1.2 on 2023-06-30 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230630_0020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='contraseña',
            new_name='password',
        ),
    ]
