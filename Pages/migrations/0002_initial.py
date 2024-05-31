# Generated by Django 5.0.2 on 2024-05-31 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Courses', '0002_initial'),
        ('Pages', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='home',
            name='featured_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Courses.course'),
        ),
        migrations.AddField(
            model_name='onboardingoption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='Pages.onboardingquestion'),
        ),
        migrations.AddField(
            model_name='step',
            name='quest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='Pages.quest'),
        ),
        migrations.AddField(
            model_name='userquestprogress',
            name='current_step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Pages.step'),
        ),
        migrations.AddField(
            model_name='userquestprogress',
            name='quest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pages.quest'),
        ),
        migrations.AddField(
            model_name='userquestprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.customuser'),
        ),
    ]