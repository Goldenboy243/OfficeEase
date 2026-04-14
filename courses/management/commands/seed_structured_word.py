from django.core.management.base import BaseCommand

from courses.models import Course, Module, Topic, Step, PracticeTask, ValidationRule


class Command(BaseCommand):
    help = "Seed Intro to Word structured course content (theory + practice + validation rules)."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name='Microsoft Word',
            defaults={
                'description': 'Learn Word from foundations to practical document creation.',
                'icon_class': 'fa-file-word',
            },
        )

        module, _ = Module.objects.get_or_create(
            course=course,
            title='Introduction Module',
            defaults={'order': 1},
        )

        topic, _ = Topic.objects.get_or_create(
            module=module,
            title='Introduction to Word',
            defaults={'order': 1, 'is_published': True},
        )

        step1, _ = Step.objects.get_or_create(
            topic=topic,
            order=1,
            defaults={
                'title': 'What is Microsoft Word?',
                'step_type': Step.THEORY,
                'content': (
                    '<p><strong>Microsoft Word</strong> is a document editor used to write, format, and share '
                    'professional documents.</p><p>In this lesson, you will understand where Word is used '
                    'and why formatting matters.</p>'
                ),
                'is_required': True,
            },
        )

        step2, _ = Step.objects.get_or_create(
            topic=topic,
            order=2,
            defaults={
                'title': 'Core Interface Basics',
                'step_type': Step.THEORY,
                'content': (
                    '<p>Word is organized around the ribbon, tabs, and the document workspace.</p>'
                    '<p>Before practical work, always identify the toolbar area, text area, and formatting controls.</p>'
                ),
                'is_required': True,
            },
        )

        step3, _ = Step.objects.get_or_create(
            topic=topic,
            order=3,
            defaults={
                'title': 'Workshop: Basic Styled Sentence',
                'step_type': Step.PRACTICE,
                'content': (
                    '<p>Now apply what you learned in a mini workshop. You must pass all tests before moving '
                    'to the next topic.</p>'
                ),
                'is_required': True,
            },
        )

        task, _ = PracticeTask.objects.get_or_create(
            step=step3,
            defaults={
                'instruction': 'Write: Hello my name is Nathan and make Nathan bold.',
                'starter_content': 'Hello my name is <b>Nathan</b>',
                'success_message': 'Excellent. You passed content and formatting checks.',
            },
        )

        ValidationRule.objects.get_or_create(
            practice_task=task,
            order=1,
            defaults={
                'name': 'Sentence Content Check',
                'rule_type': ValidationRule.CONTAINS_TEXT,
                'expected_value': 'Hello my name is Nathan',
                'is_required': True,
            },
        )

        ValidationRule.objects.get_or_create(
            practice_task=task,
            order=2,
            defaults={
                'name': 'Bold Formatting Check',
                'rule_type': ValidationRule.BOLD_TEXT,
                'expected_value': 'Nathan',
                'is_required': True,
            },
        )

        self.stdout.write(self.style.SUCCESS('Seeded structured Word introduction successfully.'))
