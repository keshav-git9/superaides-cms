# Generated by Django 5.1.4 on 2025-03-14 09:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_alter_navigroupspages_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='contents',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
