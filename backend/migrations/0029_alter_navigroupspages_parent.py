# Generated by Django 5.1.4 on 2025-03-12 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_alter_navigroupspages_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigroupspages',
            name='parent',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='backend.navigroupspages'),
        ),
    ]
