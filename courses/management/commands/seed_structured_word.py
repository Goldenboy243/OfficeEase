from django.core.management.base import BaseCommand

from courses.models import Course, Module, Step, Topic


class Command(BaseCommand):
    help = "Seed a 3-module Microsoft Word structured curriculum (theory + MCQs + workshop)."

    @staticmethod
    def _mcq_count_for_theory(theory_text):
        words = len((theory_text or "").split())
        if words >= 260:
            return 2
        return 1

    def _build_quiz_steps(self, topic, start_order, mcqs):
        order = start_order
        for mcq in mcqs:
            Step.objects.create(
                topic=topic,
                title=mcq['title'],
                step_type=Step.QUIZ,
                quiz_question=mcq['question'],
                quiz_option_1=mcq['option_1'],
                quiz_option_2=mcq['option_2'],
                quiz_correct_answer=mcq['correct'],
                content="",
                order=order,
                is_required=True,
            )
            order += 1
        return order

    def _create_module_path(self, course, title, order, theory_1, theory_2, mcq_bank, workshop_html):
        module = Module.objects.create(course=course, title=title, order=order)
        topic = module.topics.order_by('order').first()
        if topic is None:
            topic = Topic.objects.create(
                module=module,
                title=f"{title} Learning Path",
                order=1,
                is_published=True,
            )
        else:
            topic.title = f"{title} Learning Path"
            topic.order = 1
            topic.is_published = True
            topic.save(update_fields=['title', 'order', 'is_published'])

        topic.steps.all().delete()

        Step.objects.create(
            topic=topic,
            title="Theory 1",
            step_type=Step.THEORY,
            content=theory_1,
            order=1,
            is_required=True,
        )
        Step.objects.create(
            topic=topic,
            title="Theory 2",
            step_type=Step.THEORY,
            content=theory_2,
            order=2,
            is_required=True,
        )

        mcq_count = self._mcq_count_for_theory(f"{theory_1} {theory_2}")
        next_order = self._build_quiz_steps(topic, 3, mcq_bank[:mcq_count])

        if mcq_count == 1:
            fallback = mcq_bank[1]
            Step.objects.create(
                topic=topic,
                title=fallback['title'],
                step_type=Step.QUIZ,
                quiz_question=fallback['question'],
                quiz_option_1=fallback['option_1'],
                quiz_option_2=fallback['option_2'],
                quiz_correct_answer=fallback['correct'],
                content="",
                order=next_order,
                is_required=True,
            )
            next_order += 1

        Step.objects.create(
            topic=topic,
            title="Workshop",
            step_type=Step.WORKSHOP,
            content=workshop_html,
            order=next_order,
            is_required=True,
        )

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name='Microsoft Word',
            defaults={
                'description': 'Learn Word from foundations to practical document creation.',
                'icon_class': 'fa-file-word',
            },
        )

        Module.objects.filter(course=course).delete()

        self._create_module_path(
            course=course,
            title='Introduction to Word',
            order=1,
            theory_1=(
                '<p>Microsoft Word is a word processing application used to create, edit, and share documents. '
                'It is used in school, offices, and business communication.</p>'
            ),
            theory_2=(
                '<p>The Word interface includes the title bar, quick access toolbar, ribbon tabs, and document '
                'workspace. Understanding these areas helps you work faster and avoid confusion.</p>'
            ),
            mcq_bank=[
                {
                    'title': 'MCQ 1',
                    'question': 'What is the primary purpose of Microsoft Word?',
                    'option_1': 'To create and format documents',
                    'option_2': 'To edit videos',
                    'correct': '0',
                },
                {
                    'title': 'MCQ 2',
                    'question': 'Which area contains tabs like Home, Insert, and Layout?',
                    'option_1': 'Status bar',
                    'option_2': 'Ribbon',
                    'correct': '1',
                },
            ],
            workshop_html=(
                '<p>Create a short personal profile document. Use a heading, one paragraph, and save it as '
                'Word_Intro_Practice.docx.</p>'
            ),
        )

        self._create_module_path(
            course=course,
            title='Basics of Formatting',
            order=2,
            theory_1=(
                '<p>Text formatting controls how content looks. The Home tab allows you to change font, size, '
                'color, and emphasis such as bold and italic.</p>'
            ),
            theory_2=(
                '<p>Paragraph formatting controls alignment, line spacing, bullets, numbering, and indentation. '
                'Use consistent formatting to improve readability and professionalism.</p>'
            ),
            mcq_bank=[
                {
                    'title': 'MCQ 1',
                    'question': 'Which tab is most used for basic text formatting?',
                    'option_1': 'Home',
                    'option_2': 'Review',
                    'correct': '0',
                },
                {
                    'title': 'MCQ 2',
                    'question': 'Which option controls distance between text lines?',
                    'option_1': 'Line spacing',
                    'option_2': 'Zoom level',
                    'correct': '0',
                },
            ],
            workshop_html=(
                '<p>Format a one-page class notice: title centered and bold, body text justified, and add a '
                'bulleted list of three points.</p>'
            ),
        )

        self._create_module_path(
            course=course,
            title='Working with Layout and Tables',
            order=3,
            theory_1=(
                '<p>Page layout settings control margins, orientation, and size. Use portrait for letters and '
                'landscape for wide content such as schedules.</p>'
            ),
            theory_2=(
                '<p>Tables organize information into rows and columns. You can insert, style, and resize tables '
                'to present structured data clearly.</p>'
            ),
            mcq_bank=[
                {
                    'title': 'MCQ 1',
                    'question': 'Where do you change margins and orientation?',
                    'option_1': 'Layout tab',
                    'option_2': 'References tab',
                    'correct': '0',
                },
                {
                    'title': 'MCQ 2',
                    'question': 'What is a main benefit of tables in Word?',
                    'option_1': 'They store videos',
                    'option_2': 'They organize data clearly',
                    'correct': '1',
                },
            ],
            workshop_html=(
                '<p>Create a weekly study timetable using a table (at least 4 columns and 5 rows), then set '
                'page orientation based on your layout choice.</p>'
            ),
        )

        self.stdout.write(self.style.SUCCESS('Seeded 3 structured Word modules successfully.'))
