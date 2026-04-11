from django.contrib import admin
from .models import Course, Module, Lesson, Question, Profile

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5 # This automatically shows 5 empty slots for your questions!
    max_num = 5

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('label', 'title', 'module')
    list_filter = ('module',)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Profile)