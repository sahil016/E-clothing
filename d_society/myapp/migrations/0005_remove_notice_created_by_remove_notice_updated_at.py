# Generated by Django 5.1.6 on 2025-03-23 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_event_notice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='notice',
            name='updated_at',
        ),
    ]
