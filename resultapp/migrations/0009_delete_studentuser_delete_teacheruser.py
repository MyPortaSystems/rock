# Generated by Django 5.0.3 on 2024-03-22 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resultapp', '0008_remove_student_user_remove_teacher_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentUser',
        ),
        migrations.DeleteModel(
            name='TeacherUser',
        ),
    ]
