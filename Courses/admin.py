from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import mark_safe
from .models import Course, Level, Module, Video, Quiz, UserCourseProgress

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 0

class VideoInline(admin.StackedInline):
    model = Video
    extra = 0

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0
    inlines = [VideoInline]

class LevelInline(admin.StackedInline):
    model = Level
    extra = 0
    inlines = [ModuleInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_image', 'professor', 'price', 'members_count']
    search_fields = ['title', 'description', 'professor__name']
    list_filter = ['price', 'professor']
    readonly_fields = ['course_image']
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'price', 'img', 'course_image', 'professor', 'members_count')
        }),
    )
    inlines = [LevelInline, ModuleInline, VideoInline, QuizInline]

    class Media:
        js = ('js/collapsible_inlines.js',)

admin.site.register(Course, CourseAdmin)

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    pass
