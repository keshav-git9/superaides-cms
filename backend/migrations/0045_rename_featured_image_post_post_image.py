# Generated by Django 5.1.4 on 2025-04-07 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0044_rename_content_post_contents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='featured_image',
            new_name='post_image',
        ),
    ]
