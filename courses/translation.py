from modeltranslation.translator import register, TranslationOptions
from .models import Course, Module, Lesson, Question, Topic, Step, PracticeTask, ValidationRule

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


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(PracticeTask)
class PracticeTaskTranslationOptions(TranslationOptions):
    fields = ('instruction', 'success_message')


@register(ValidationRule)
class ValidationRuleTranslationOptions(TranslationOptions):
    fields = ('name', 'expected_value')
