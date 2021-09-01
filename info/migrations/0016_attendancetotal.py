# Generated by Django 3.1.2 on 2020-11-07 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0015_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.student')),
            ],
        ),
    ]