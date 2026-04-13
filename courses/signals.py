from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Course, Module, Lesson, Question, Topic, Step, PracticeTask, ValidationRule
from deep_translator import GoogleTranslator

# Helper to automatically translate specific fields
def auto_translate(instance, fields):
    targets = ['fr', 'my', 'hi']
    for field in fields:
        original_text = getattr(instance, f'{field}_en', None)
        if not original_text:
            continue
            
        for lang in targets:
            dest_field = f'{field}_{lang}'
            current_dest = getattr(instance, dest_field, None)
            
            # If the destination translation field is empty, automatically translate it
            if not current_dest:
                try:
                    translated = GoogleTranslator(source='en', target=lang).translate(original_text)
                    setattr(instance, dest_field, translated)
                except Exception as e:
                    print(f"Auto-translation error to {lang} for {field}: {e}")

@receiver(pre_save, sender=Course)
def translate_course(sender, instance, **kwargs):
    auto_translate(instance, ['name', 'description'])

@receiver(pre_save, sender=Module)
def translate_module(sender, instance, **kwargs):
    auto_translate(instance, ['title'])

@receiver(pre_save, sender=Lesson)
def translate_lesson(sender, instance, **kwargs):
    auto_translate(instance, ['title', 'theory'])

@receiver(pre_save, sender=Question)
def translate_question(sender, instance, **kwargs):
    auto_translate(instance, ['question_text', 'option_1', 'option_2'])


@receiver(pre_save, sender=Topic)
def translate_topic(sender, instance, **kwargs):
    auto_translate(instance, ['title'])


@receiver(pre_save, sender=Step)
def translate_step(sender, instance, **kwargs):
    auto_translate(instance, ['title', 'content'])


@receiver(pre_save, sender=PracticeTask)
def translate_practice_task(sender, instance, **kwargs):
    auto_translate(instance, ['instruction', 'success_message'])


@receiver(pre_save, sender=ValidationRule)
def translate_validation_rule(sender, instance, **kwargs):
    auto_translate(instance, ['name', 'expected_value'])
