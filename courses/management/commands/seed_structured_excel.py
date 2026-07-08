from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, pre_save

from courses.models import Course, Lesson, Module, Question
from courses import signals as course_signals


class Command(BaseCommand):
    help = "Seed a 3-module Microsoft Excel course with lessons and quiz questions."

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

        for index, question_data in enumerate(questions, start=1):
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
                name='Microsoft Excel',
                defaults={
                    'description': 'Learn Excel from workbook basics to formulas, charts, and data analysis.',
                    'icon_class': 'fa-file-excel',
                },
            )

            Module.objects.filter(course=course).delete()

            self._create_module(
                course=course,
                title='Excel Foundations',
                order=1,
                lessons=[
                    {
                        'label': '1.1',
                        'title': 'Getting Started with Excel',
                        'theory': (
                            '<p>Microsoft Excel is a spreadsheet program used to organize data, perform calculations, '
                            'and create reports. Worksheets are made up of rows, columns, and cells.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What is Excel primarily used for?',
                                'option_1': 'Calculations and data organization',
                                'option_2': 'Video editing',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '1.2',
                        'title': 'Workbook Layout',
                        'theory': (
                            '<p>An Excel workbook contains one or more worksheets. Each worksheet is built from '
                            'cells identified by a column letter and row number, such as A1 or B5.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What identifies a single cell in Excel?',
                                'option_1': 'A row and column reference like A1',
                                'option_2': 'A slide number',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self._create_module(
                course=course,
                title='Formulas and Formatting',
                order=2,
                lessons=[
                    {
                        'label': '2.1',
                        'title': 'Using Basic Formulas',
                        'theory': (
                            '<p>Formulas in Excel start with an equals sign. Common formulas include SUM, AVERAGE, and '
                            'COUNT, which help automate repeated calculations.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What symbol starts every Excel formula?',
                                'option_1': 'An equals sign (=)',
                                'option_2': 'A hashtag (#)',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '2.2',
                        'title': 'Formatting Data Clearly',
                        'theory': (
                            '<p>Formatting helps data become easier to read. You can adjust fonts, apply number formats, '
                            'and highlight important cells with colors and borders.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'Why is formatting important in Excel?',
                                'option_1': 'It makes data easier to read and understand',
                                'option_2': 'It deletes worksheets',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self._create_module(
                course=course,
                title='Tables and Charts',
                order=3,
                lessons=[
                    {
                        'label': '3.1',
                        'title': 'Working with Tables',
                        'theory': (
                            '<p>Tables help you sort, filter, and manage structured data. Converting a range into a '
                            'table makes large datasets easier to explore.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'What is a key benefit of Excel tables?',
                                'option_1': 'They help sort and filter data',
                                'option_2': 'They turn data into images',
                                'correct_answer': '0',
                            },
                        ],
                    },
                    {
                        'label': '3.2',
                        'title': 'Creating Charts',
                        'theory': (
                            '<p>Charts convert raw numbers into visuals like bar charts and pie charts. They help '
                            'communicate trends and comparisons quickly.</p>'
                        ),
                        'questions': [
                            {
                                'question_text': 'Why do people use charts in Excel?',
                                'option_1': 'To display trends and comparisons visually',
                                'option_2': 'To write long essays',
                                'correct_answer': '0',
                            },
                        ],
                    },
                ],
            )

            self.stdout.write(self.style.SUCCESS('Seeded Microsoft Excel course successfully.'))
        finally:
            self._restore_signals()