# Generated by Django 3.1.2 on 2020-10-30 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_marksclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksclass',
            name='examname',
            field=models.CharField(max_length=10),
        ),
        migrations.CreateModel(
            name='EnterMarks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.CharField(max_length=20)),
                ('marksclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.marksclass')),
                ('stud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.student')),
            ],
        ),
    ]