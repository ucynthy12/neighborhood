# Generated by Django 3.1.5 on 2021-01-29 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0003_auto_20210129_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='neighborhood',
            new_name='hood',
        ),
    ]