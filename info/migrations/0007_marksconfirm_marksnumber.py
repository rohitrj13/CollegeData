# Generated by Django 3.1.2 on 2020-10-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_marksconfirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='marksconfirm',
            name='marksnumber',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
