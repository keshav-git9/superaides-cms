# Generated by Django 5.2.3 on 2025-06-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0067_navigroupspages_page_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
