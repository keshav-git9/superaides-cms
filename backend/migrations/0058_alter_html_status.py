# Generated by Django 5.1.4 on 2025-04-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0057_alter_customuser_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='html',
            name='status',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
