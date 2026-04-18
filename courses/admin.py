from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Course,
    Module,
    Lesson,
    Question,
    Topic,
    Step,
    PracticeTask,
    ValidationRule,
    UserStepProgress,
    PracticeSubmission,
    WorkshopSubmission,
)

class QuestionInline(TranslationTabularInline):
    model = Question
    extra = 5 # This automatically shows 5 empty slots for your questions!
    max_num = 5

class LessonAdmin(TranslationAdmin):
    inlines = [QuestionInline]
    list_display = ('label', 'title', 'module')
    list_filter = ('module',)


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    fields = (
        'title',
        'step_type',
        'content',
        'quiz_question',
        'quiz_option_1',
        'quiz_option_2',
        'quiz_correct_answer',
        'workshop_required_text',
        'workshop_min_words',
        'order',
        'is_required',
    )


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_published')
    list_filter = ('module__course', 'module', 'is_published')
    inlines = [StepInline]


class ValidationRuleInline(admin.TabularInline):
    model = ValidationRule
    extra = 1


class PracticeTaskAdmin(admin.ModelAdmin):
    list_display = ('step', 'instruction')
    list_filter = ('step__topic__module__course',)
    inlines = [ValidationRuleInline]


class UserStepProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'step', 'status', 'completed_at')
    list_filter = ('status', 'step__topic__module__course')


class PracticeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'step', 'is_passed', 'created_at')
    list_filter = ('is_passed', 'step__topic__module__course')


class WorkshopSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'step', 'is_passed', 'created_at')
    list_filter = ('is_passed', 'step__topic__module__course')

class ModuleAdmin(TranslationAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

class CourseAdmin(TranslationAdmin):
    list_display = ('name', 'icon_class')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(PracticeTask, PracticeTaskAdmin)
admin.site.register(UserStepProgress, UserStepProgressAdmin)
admin.site.register(PracticeSubmission, PracticeSubmissionAdmin)
admin.site.register(WorkshopSubmission, WorkshopSubmissionAdmin)
