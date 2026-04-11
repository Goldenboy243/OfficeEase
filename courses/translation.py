from modeltranslation.translator import register, TranslationOptions
from .models import Course, Module, Lesson, Question

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Module)
class ModuleTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'theory')

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question_text', 'option_1', 'option_2')
