# Generated by Django 3.1.2 on 2023-07-02 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tipouser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tipo',
        ),
        migrations.DeleteModel(
            name='TipoUser',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]