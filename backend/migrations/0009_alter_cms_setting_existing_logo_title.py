# Generated by Django 5.1.4 on 2025-01-08 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_cms_setting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cms_setting',
            name='existing_logo_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
