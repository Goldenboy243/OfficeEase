from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, pre_save

from courses.models import Course, Lesson, Module, Question
from courses import signals as course_signals


class Command(BaseCommand):
    help = "Seed a 3-module Microsoft PowerPoint course with lessons and quiz questions."

    def _mute_signals(self):
        pre_save.disconnect(course_signals.translate_course, sender=Course)
        pre_save.disconnect(course_signals.translate_module, sender=Module)
        pre_save.disconnect(course_signals.translate_lesson, sender=Lesson)
        pre_save.disconnect(course_signals.translate_question, sender=Question)
        post_save.disconnect(course_signals.bootstrap_module_structure, sender=Module)

    def _restore_signals(self):
        pre_save.connect(course_signals.translate_course, sender=Course)
        pre_save.connect(course_signals.translate_module, sender=Module)
        pre_save.connect(course_signals.translate_lesson, sender=Lesson)
        pre_save.connect(course_signals.translate_question, sender=Question)
        post_save.connect(course_signals.bootstrap_module_structure, sender=Module)

    def _create_lesson(self, module, label, title, theory, embed_url, order, questions):
        lesson = Lesson.objects.create(
            module=module,
            label=label,
            title=title,
            theory=theory,
            embed_url=embed_url,
            order=order,
        )

        for question_data in questions:
            Question.objects.create(
                lesson=lesson,
                question_text=question_data['question_text'],
                option_1=question_data['option_1'],
                option_2=question_data['option_2'],
                correct_answer=question_data['correct_answer'],
            )

        return lesson

    def _create_module(self, course, title, order, lessons):
        module = Module.objects.create(course=course, title=title, order=order)
        for lesson_index, lesson_data in enumerate(lessons, start=1):
            self._create_lesson(
                module=module,
                label=lesson_data['label'],
                title=lesson_data['title'],
                theory=lesson_data['theory'],
                embed_url=lesson_data.get('embed_url'),
                order=lesson_index,
                questions=lesson_data['questions'],
            )

    def handle(self, *args, **options):
        self._mute_signals()
        try:
            course, _ = Course.objects.get_or_create(
                name='Microsoft PowerPoint',
                defaults={
                    'description': 'Learn PowerPoint from slide basics to presentation design and delivery.',
                    'icon_class': 'fa-file-powerpoint',
                },
            )

            Module.objects.filter(course=course).delete()

            self._create_module(
                course=course,
                title='PowerPoint Foundations',
                order=1,
                lessons=[
                    {
                        'label': '1.1',
                        'title': 'Getting Started with Slides',
                        'theory': (
                            '<p>Microsoft PowerPoint is used to create slide-based presentations. Each presentation is '
                            'built from slides that can include text, images, charts, and video.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What is a PowerPoint presentation made of?',
                                'option_1': 'Slides',
                                'option_2': 'Cells',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '1.2',
                        'title': 'Themes and Layouts',
                        'theory': (
                            '<p>Themes control the overall look of a presentation, while layouts decide where titles, '
                            'text, and other elements appear on each slide.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What does a slide layout control?',
                                'option_1': 'Where slide elements are placed',
                                'option_2': 'How fast the computer runs',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self._create_module(
                course=course,
                title='Designing Effective Slides',
                order=2,
                lessons=[
                    {
                        'label': '2.1',
                        'title': 'Text and Visual Balance',
                        'theory': (
                            '<p>Good slides keep text short and use visuals to support the message. Too much text makes '
                            'a slide hard to follow.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'Why should slides avoid too much text?',
                                'option_1': 'So the audience can follow the message more easily',
                                'option_2': 'So they look empty',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '2.2',
                        'title': 'Animations and Transitions',
                        'theory': (
                            '<p>Animations and transitions can make presentations more engaging when used carefully. '
                            'They should support the content, not distract from it.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What should animations do in a presentation?',
                                'option_1': 'Support the message without distracting',
                                'option_2': 'Replace all slide content',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self._create_module(
                course=course,
                title='Presenting with Confidence',
                order=3,
                lessons=[
                    {
                        'label': '3.1',
                        'title': 'Speaker Notes and Rehearsal',
                        'theory': (
                            '<p>Speaker notes help you remember key points while presenting. Rehearsing lets you '
                            'check timing and improve delivery before the live presentation.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'Why use speaker notes?',
                                'option_1': 'To remember key points during a presentation',
                                'option_2': 'To hide the slides',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '3.2',
                        'title': 'Final Presentation Tips',
                        'theory': (
                            '<p>Clear voice, simple slides, and a steady pace help you present with confidence. '
                            'Strong structure and practice improve audience understanding.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What helps a presentation feel clear and confident?',
                                'option_1': 'Practice and a simple slide structure',
                                'option_2': 'Very long paragraphs on every slide',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self.stdout.write(self.style.SUCCESS('Seeded Microsoft PowerPoint course successfully.'))
        finally:
            self._restore_signals()