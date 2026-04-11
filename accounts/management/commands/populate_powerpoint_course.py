from django.core.management.base import BaseCommand
from accounts.models import Course, Module, Lesson, Question


class Command(BaseCommand):
    help = 'Populate the database with sample PowerPoint course data'

    def handle(self, *args, **options):
        # Create or get PowerPoint course
        course, created = Course.objects.get_or_create(
            name="Microsoft PowerPoint",
            defaults={
                'description': 'Learn Microsoft PowerPoint from basics to advanced presentations',
                'icon_class': 'fa-file-powerpoint'
            }
        )
        
        if not created:
            self.stdout.write(self.style.WARNING('PowerPoint course already exists'))
            return

        # Module 1: Getting Started
        module1 = Module.objects.create(
            course=course,
            title='1. Introduction to PowerPoint',
            order=1
        )

        lesson1_1 = Lesson.objects.create(
            module=module1,
            label='1.1',
            title='Understanding PowerPoint Basics',
            theory='''
                <h3>What is PowerPoint?</h3>
                <p>Microsoft PowerPoint is a presentation software that helps you create, edit, and present slideshows with text, images, and multimedia.</p>
                <h4>Key Components:</h4>
                <ul>
                    <li><strong>Slides:</strong> Individual pages in your presentation</li>
                    <li><strong>Ribbon:</strong> Contains formatting tools and commands</li>
                    <li><strong>Outline/Slide Pane:</strong> Shows thumbnails of all slides</li>
                    <li><strong>Notes Section:</strong> Speaker notes area below the slide</li>
                    <li><strong>Slide Sorter:</strong> View all slides at once for organization</li>
                </ul>
                <p><strong>File Format:</strong> PowerPoint files use .PPTX extension (older versions use .PPT)</p>
            ''',
            embed_url='https://example.com/ppt-basics',
            order=1
        )

        Question.objects.create(
            lesson=lesson1_1,
            question_text='What is the file extension for modern PowerPoint presentations?',
            option_1='.PPT',
            option_2='.PPTX',
            correct_answer='1'
        )

        Question.objects.create(
            lesson=lesson1_1,
            question_text='What is the primary purpose of PowerPoint?',
            option_1='Create documents and reports',
            option_2='Create and present slideshows',
            correct_answer='1'
        )

        lesson1_2 = Lesson.objects.create(
            module=module1,
            label='1.2',
            title='Creating Your First Presentation',
            theory='''
                <h3>Getting Started</h3>
                <p>Creating a presentation in PowerPoint is simple and intuitive.</p>
                <ol>
                    <li>Open PowerPoint and select "Blank Presentation"</li>
                    <li>Choose a slide layout (Title Slide, Title and Content, etc.)</li>
                    <li>Click on text placeholders to add your content</li>
                    <li>Add more slides with the "New Slide" button</li>
                    <li>Customize with colors, fonts, and images</li>
                </ol>
                <h4>Slide Layouts:</h4>
                <ul>
                    <li><strong>Title Slide:</strong> For the first slide with title and subtitle</li>
                    <li><strong>Title and Content:</strong> Title with bullet points</li>
                    <li><strong>Blank:</strong> Empty slide for custom design</li>
                    <li><strong>Two Content:</strong> Side-by-side content areas</li>
                </ul>
                <p><strong>Tip:</strong> Use Ctrl+M to add a new slide quickly.</p>
            ''',
            embed_url='https://example.com/ppt-first-pres',
            order=2
        )

        Question.objects.create(
            lesson=lesson1_2,
            question_text='Which keyboard shortcut adds a new slide?',
            option_1='Ctrl+N',
            option_2='Ctrl+M',
            correct_answer='1'
        )

        Question.objects.create(
            lesson=lesson1_2,
            question_text='What is the "Title Slide" layout used for?',
            option_1='Every slide in the presentation',
            option_2='The first slide with title and subtitle',
            correct_answer='1'
        )

        # Module 2: Designing Slides
        module2 = Module.objects.create(
            course=course,
            title='2. Designing Professional Slides',
            order=2
        )

        lesson2_1 = Lesson.objects.create(
            module=module2,
            label='2.1',
            title='Formatting Text and Shapes',
            theory='''
                <h3>Making Your Slides Look Professional</h3>
                <p>Good design is crucial for engaging presentations.</p>
                <h4>Text Formatting:</h4>
                <ul>
                    <li>Use 2-3 font types maximum across the presentation</li>
                    <li>Keep font size readable: 44pt for titles, 32pt for body text</li>
                    <li>Use bold and colors to highlight key points</li>
                    <li>Proper alignment (left, center, or right)</li>
                </ul>
                <h4>Adding Shapes:</h4>
                <ul>
                    <li>Rectangles, circles, and arrows for emphasis</li>
                    <li>Shape effects like shadows and 3D</li>
                    <li>Grouping shapes for complex designs</li>
                    <li>Using SmartArt for diagrams</li>
                </ul>
                <p><strong>Best Practice:</strong> Less is more. Don't clutter your slides.</p>
            ''',
            embed_url='https://example.com/ppt-formatting',
            order=1
        )

        Question.objects.create(
            lesson=lesson2_1,
            question_text='What is the recommended font size for body text in PowerPoint?',
            option_1='18pt',
            option_2='32pt',
            correct_answer='1'
        )

        Question.objects.create(
            lesson=lesson2_1,
            question_text='How many different fonts is recommended per presentation?',
            option_1='2-3 maximum',
            option_2='As many as you want',
            correct_answer='0'
        )

        lesson2_2 = Lesson.objects.create(
            module=module2,
            label='2.2',
            title='Using Themes and Colors',
            theory='''
                <h3>Consistent Design with Themes</h3>
                <p>PowerPoint themes ensure your presentation looks polished and professional.</p>
                <h4>What is a Theme?</h4>
                <p>A theme is a collection of:</p>
                <ul>
                    <li>Color schemes (set of complementary colors)</li>
                    <li>Fonts (title and body text)</li>
                    <li>Layout designs (background elements)</li>
                    <li>Effects (animations and transitions)</li>
                </ul>
                <h4>Applying Themes:</h4>
                <ol>
                    <li>Go to Design tab</li>
                    <li>Browse available themes</li>
                    <li>Click to apply instantly</li>
                    <li>Customize colors and fonts if needed</li>
                </ol>
                <p><strong>Color Psychology:</strong> Blue = Trust, Red = Energy, Green = Growth, Yellow = Optimism</p>
            ''',
            embed_url='https://example.com/ppt-themes',
            order=2
        )

        Question.objects.create(
            lesson=lesson2_2,
            question_text='What does a PowerPoint theme include?',
            option_1='Only colors',
            option_2='Color schemes, fonts, layouts, and effects',
            correct_answer='1'
        )

        Question.objects.create(
            lesson=lesson2_2,
            question_text='Which color suggests trust and stability?',
            option_1='Blue',
            option_2='Red',
            correct_answer='0'
        )

        # Module 3: Advanced Presentations
        module3 = Module.objects.create(
            course=course,
            title='3. Advanced Features',
            order=3
        )

        lesson3_1 = Lesson.objects.create(
            module=module3,
            label='3.1',
            title='Animations and Transitions',
            theory='''
                <h3>Making Your Presentation Dynamic</h3>
                <p>Animations and transitions add movement and professionalism to your slides.</p>
                <h4>Transitions:</h4>
                <p>Transitions control how you move from one slide to the next.</p>
                <ul>
                    <li>Fade, Push, Wipe, and Zoom effects</li>
                    <li>Adjust transition speed and timing</li>
                    <li>Add sound effects</li>
                    <li>Set automatic advance timing</li>
                </ul>
                <h4>Animations:</h4>
                <p>Animations control how elements appear within a slide.</p>
                <ul>
                    <li><strong>Entrance:</strong> Fade In, Fly In, Bounce</li>
                    <li><strong>Emphasis:</strong> Grow/Shrink, Color Pulse, Spin</li>
                    <li><strong>Exit:</strong> Fade Out, Fly Out, Dissolve</li>
                    <li>Trigger animations on click or by timing</li>
                </ul>
                <p><strong>Warning:</strong> Avoid excessive animations - they distract from content.</p>
            ''',
            embed_url='https://example.com/ppt-animations',
            order=1
        )

        Question.objects.create(
            lesson=lesson3_1,
            question_text='What is the difference between transitions and animations?',
            option_1='Transitions go between slides, animations are within slides',
            option_2='They are the same thing',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson3_1,
            question_text='What is an entrance animation?',
            option_1='How an object appears in a slide',
            option_2='How one slide changes to the next',
            correct_answer='0'
        )

        lesson3_2 = Lesson.objects.create(
            module=module3,
            label='3.2',
            title='Presenting and Publishing',
            theory='''
                <h3>Delivering Your Presentation</h3>
                <p>PowerPoint offers various ways to present and share your work.</p>
                <h4>Presentation Modes:</h4>
                <ul>
                    <li><strong>Normal View:</strong> Editing mode</li>
                    <li><strong>Slide Sorter:</strong> See all slides at once</li>
                    <li><strong>Presenter View:</strong> See notes and upcoming slides</li>
                    <li><strong>Slideshow:</strong> Full-screen presentation (F5 to start)</li>
                </ul>
                <h4>Publishing Options:</h4>
                <ul>
                    <li>Save as PDF for universal compatibility</li>
                    <li>Export as video for social media</li>
                    <li>Share online with PowerPoint Online</li>
                    <li>Print handouts for distribution</li>
                </ul>
                <h4>Presentation Tips:</h4>
                <ul>
                    <li>Use Presenter Notes for speaker reminders</li>
                    <li>Practice before presenting</li>
                    <li>Use a remote clicker for navigation</li>
                    <li>Maintain eye contact with the audience</li>
                </ul>
            ''',
            embed_url='https://example.com/ppt-presenting',
            order=2
        )

        Question.objects.create(
            lesson=lesson3_2,
            question_text='What keyboard shortcut starts a slideshow in PowerPoint?',
            option_1='F5',
            option_2='Ctrl+F5',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson3_2,
            question_text='Which format should you use to ensure compatibility across devices?',
            option_1='PDF',
            option_2='.PPTX only',
            correct_answer='0'
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created PowerPoint course with {Module.objects.filter(course=course).count()} modules'
            )
        )
