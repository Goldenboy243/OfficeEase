from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Course, Module, Lesson, Question

class QuestionInline(TranslationTabularInline):
    model = Question
    extra = 5 # This automatically shows 5 empty slots for your questions!
    max_num = 5

class LessonAdmin(TranslationAdmin):
    inlines = [QuestionInline]
    list_display = ('label', 'title', 'module')
    list_filter = ('module',)

class ModuleAdmin(TranslationAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

class CourseAdmin(TranslationAdmin):
    list_display = ('name', 'icon_class')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
