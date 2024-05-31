# Generated by Django 5.0.2 on 2024-05-31 09:31

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('discount_price', models.IntegerField(blank=True, default=0, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='Course_img')),
                ('members_count', models.IntegerField(default=0)),
                ('course_requirements', models.TextField(blank=True, null=True)),
                ('course_features', models.TextField(blank=True, null=True)),
                ('video_trailer', models.FileField(blank=True, null=True, upload_to='course_trailers')),
                ('category', models.CharField(choices=[('Trading', 'Trading'), ('Development', 'Development'), ('Design', 'Design UI / UX'), ('Data Science', 'Data Science'), ('Marketing', 'Marketing')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseProgression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='levels_images')),
                ('level_number', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelProgression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('index', models.IntegerField(default=0)),
                ('module_number', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.CharField(max_length=255)),
                ('option1_img', models.ImageField(blank=True, null=True, upload_to='quiz_images')),
                ('option2', models.CharField(max_length=255)),
                ('option2_img', models.ImageField(blank=True, null=True, upload_to='quiz_images')),
                ('option3', models.CharField(max_length=255)),
                ('option3_img', models.ImageField(blank=True, null=True, upload_to='quiz_images')),
                ('option4', models.CharField(max_length=255)),
                ('option4_img', models.ImageField(blank=True, null=True, upload_to='quiz_images')),
                ('answer', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='coursesVideos')),
                ('summary', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('notes', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
    ]
