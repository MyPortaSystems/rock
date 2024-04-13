# Generated by Django 5.0.3 on 2024-03-22 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultapp', '0006_remove_class_student_class_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='class',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
        migrations.AlterField(
            model_name='result',
            name='total_scores',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultapp.studentuser'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultapp.teacheruser'),
        ),
    ]