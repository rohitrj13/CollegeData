# Generated by Django 3.1.2 on 2020-11-02 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_auto_20201102_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marksconfirm',
            name='att',
        ),
        migrations.RemoveField(
            model_name='marksconfirm',
            name='status',
        ),
    ]
