# Generated by Django 5.1.6 on 2025-03-13 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_user_email_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('chairman', 'Chairman'), ('member', 'Member'), ('visitor', 'Visitor'), ('watchman', 'Watchman')], default='member', max_length=20),
        ),
    ]
