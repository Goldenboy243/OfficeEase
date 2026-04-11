from django.core.management.base import BaseCommand
from accounts.models import Course, Module, Lesson, Question


class Command(BaseCommand):
    help = 'Populate the database with sample Excel course data'

    def handle(self, *args, **options):
        # Create or get Excel course
        course, created = Course.objects.get_or_create(
            name="Microsoft Excel",
            defaults={
                'description': 'Learn Microsoft Excel from basics to advanced',
                'icon_class': 'fa-file-excel'
            }
        )
        
        if not created:
            self.stdout.write(self.style.WARNING('Excel course already exists'))
            return

        # Module 1: Getting Started
        module1 = Module.objects.create(
            course=course,
            title='1. Getting Started with Excel',
            order=1
        )

        lesson1_1 = Lesson.objects.create(
            module=module1,
            label='1.1',
            title='Understanding the Excel Interface',
            theory='''
                <h3>The Excel Interface</h3>
                <p>Microsoft Excel is a spreadsheet application that organizes data in rows and columns.</p>
                <ul>
                    <li><strong>Ribbon:</strong> Contains tools and commands at the top</li>
                    <li><strong>Name Box:</strong> Shows the current cell reference</li>
                    <li><strong>Formula Bar:</strong> Displays the formula or content of the selected cell</li>
                    <li><strong>Worksheet:</strong> Grid of cells where you enter data</li>
                    <li><strong>Sheet Tabs:</strong> Navigate between different worksheets</li>
                </ul>
                <p>Each cell has a reference like A1, B2, etc., where the letter represents the column and the number represents the row.</p>
            ''',
            embed_url='https://example.com/excel-intro',
            order=1
        )

        Question.objects.create(
            lesson=lesson1_1,
            question_text='What does the letter in a cell reference represent?',
            option_1='The column',
            option_2='The row',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson1_1,
            question_text='Where would you find the formula bar in Excel?',
            option_1='At the top of the screen below the Ribbon',
            option_2='At the bottom of the screen',
            correct_answer='0'
        )

        lesson1_2 = Lesson.objects.create(
            module=module1,
            label='1.2',
            title='Creating Your First Spreadsheet',
            theory='''
                <h3>Creating a New Spreadsheet</h3>
                <p>To start creating a spreadsheet in Excel:</p>
                <ol>
                    <li>Open Microsoft Excel</li>
                    <li>Select "Blank workbook" or use Ctrl+N</li>
                    <li>Click on a cell to start entering data</li>
                    <li>Type your data and press Enter to move to the next cell</li>
                    <li>Use Tab to move right or Shift+Tab to move left</li>
                </ol>
                <p><strong>Tips:</strong></p>
                <ul>
                    <li>You can edit a cell by pressing F2 or double-clicking it</li>
                    <li>Press Escape to cancel any changes</li>
                    <li>Use Ctrl+S to save your work</li>
                </ul>
            ''',
            embed_url='https://example.com/excel-first-sheet',
            order=2
        )

        Question.objects.create(
            lesson=lesson1_2,
            question_text='How do you move to the next row after entering data in a cell?',
            option_1='Press Enter',
            option_2='Press Tab',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson1_2,
            question_text='Which keyboard shortcut creates a new workbook?',
            option_1='Ctrl+N',
            option_2='Ctrl+O',
            correct_answer='0'
        )

        # Module 2: Formatting
        module2 = Module.objects.create(
            course=course,
            title='2. Formatting Cells and Data',
            order=2
        )

        lesson2_1 = Lesson.objects.create(
            module=module2,
            label='2.1',
            title='Cell Formatting Basics',
            theory='''
                <h3>Formatting Cells</h3>
                <p>Excel allows you to format cells to make your data more readable and professional.</p>
                <h4>Common Formatting Options:</h4>
                <ul>
                    <li><strong>Font:</strong> Change font type, size, and style (bold, italic, underline)</li>
                    <li><strong>Color:</strong> Change text color and cell background color</li>
                    <li><strong>Alignment:</strong> Left, center, right, or justify text</li>
                    <li><strong>Number Format:</strong> Display as currency, percentage, date, etc.</li>
                    <li><strong>Borders:</strong> Add borders around cells</li>
                </ul>
                <p>To format cells, select them and use the Format Cells dialog (Ctrl+1) or the formatting options in the Home tab.</p>
            ''',
            embed_url='https://example.com/excel-formatting',
            order=1
        )

        Question.objects.create(
            lesson=lesson2_1,
            question_text='How do you open the Format Cells dialog?',
            option_1='Ctrl+1',
            option_2='Ctrl+Shift+F',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson2_1,
            question_text='Which of the following is NOT a common cell formatting option?',
            option_1='Cell rotation',
            option_2='Word wrap',
            correct_answer='1'
        )

        lesson2_2 = Lesson.objects.create(
            module=module2,
            label='2.2',
            title='Number and Date Formatting',
            theory='''
                <h3>Working with Numbers and Dates</h3>
                <p>Excel uses specific formats to display numbers and dates correctly.</p>
                <h4>Number Formats:</h4>
                <ul>
                    <li><strong>Currency:</strong> Displays numbers with a currency symbol ($, €, £)</li>
                    <li><strong>Percentage:</strong> Multiplies by 100 and adds % symbol</li>
                    <li><strong>Decimal:</strong> Controls decimal places shown</li>
                    <li><strong>Thousands Separator:</strong> Adds commas for readability</li>
                </ul>
                <h4>Date Formats:</h4>
                <p>Dates can be displayed as MM/DD/YYYY, DD/MM/YYYY, Month Day, Year, or custom formats.</p>
                <p>Select the cells, right-click, choose "Format Cells", then select the Number tab to apply formats.</p>
            ''',
            embed_url='https://example.com/excel-numbers-dates',
            order=2
        )

        Question.objects.create(
            lesson=lesson2_2,
            question_text='What does the percentage format do to a number like 0.5?',
            option_1='Displays it as 50%',
            option_2='Displays it as 0.5%',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson2_2,
            question_text='Which format would you use to display $1,234.56?',
            option_1='Currency',
            option_2='Decimal',
            correct_answer='0'
        )

        # Module 3: Formulas
        module3 = Module.objects.create(
            course=course,
            title='3. Working with Formulas',
            order=3
        )

        lesson3_1 = Lesson.objects.create(
            module=module3,
            label='3.1',
            title='Introduction to Formulas',
            theory='''
                <h3>Understanding Formulas</h3>
                <p>Formulas are the core of Excel. They allow you to perform calculations and data analysis.</p>
                <h4>Formula Basics:</h4>
                <ul>
                    <li>All formulas start with an equals sign (=)</li>
                    <li>Formulas can reference cells (e.g., =A1+B1)</li>
                    <li>Formulas can contain functions (e.g., =SUM(A1:A10))</li>
                    <li>Formulas are calculated automatically</li>
                </ul>
                <h4>Common Operators:</h4>
                <ul>
                    <li>+ (Addition): =A1+B1</li>
                    <li>- (Subtraction): =A1-B1</li>
                    <li>* (Multiplication): =A1*B1</li>
                    <li>/ (Division): =A1/B1</li>
                    <li>^ (Exponent): =A1^2</li>
                </ul>
            ''',
            embed_url='https://example.com/excel-formulas',
            order=1
        )

        Question.objects.create(
            lesson=lesson3_1,
            question_text='What character must every formula start with?',
            option_1='The equals sign (=)',
            option_2='The dollar sign ($)',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson3_1,
            question_text='Which symbol is used for multiplication in Excel?',
            option_1='x',
            option_2='*',
            correct_answer='1'
        )

        lesson3_2 = Lesson.objects.create(
            module=module3,
            label='3.2',
            title='Essential Functions',
            theory='''
                <h3>Common Excel Functions</h3>
                <p>Excel has built-in functions that perform predefined calculations.</p>
                <h4>Math Functions:</h4>
                <ul>
                    <li><strong>SUM:</strong> =SUM(A1:A10) - Adds all values</li>
                    <li><strong>AVERAGE:</strong> =AVERAGE(A1:A10) - Calculates the mean</li>
                    <li><strong>COUNT:</strong> =COUNT(A1:A10) - Counts cells with numbers</li>
                    <li><strong>MIN:</strong> =MIN(A1:A10) - Finds the smallest value</li>
                    <li><strong>MAX:</strong> =MAX(A1:A10) - Finds the largest value</li>
                </ul>
                <h4>Text Functions:</h4>
                <ul>
                    <li><strong>CONCATENATE:</strong> Joins text together</li>
                    <li><strong>LEN:</strong> Counts characters in text</li>
                    <li><strong>UPPER:</strong> Converts text to uppercase</li>
                    <li><strong>LOWER:</strong> Converts text to lowercase</li>
                </ul>
                <p>Functions use a range (A1:A10) or individual cells as arguments.</p>
            ''',
            embed_url='https://example.com/excel-functions',
            order=2
        )

        Question.objects.create(
            lesson=lesson3_2,
            question_text='What function calculates the average of a range?',
            option_1='AVERAGE',
            option_2='AVG',
            correct_answer='0'
        )

        Question.objects.create(
            lesson=lesson3_2,
            question_text='Which function counts the number of cells with numbers?',
            option_1='COUNTA',
            option_2='COUNT',
            correct_answer='1'
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created Excel course with {Module.objects.filter(course=course).count()} modules'
            )
        )
