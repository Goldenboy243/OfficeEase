from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=100) # e.g., Microsoft Word
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default="fa-file-word") # For font-awesome icons

    def __str__(self):
        return self.name

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200) # e.g., 1. Introduction & Basic Navigation
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    label = models.CharField(max_length=10) # e.g., 1.1
    title = models.CharField(max_length=200) # e.g., The Ribbon Interface
    theory = models.TextField() # You can put HTML content here
    embed_url = models.URLField(max_length=500, blank=True, null=True) # Your OneDrive link
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} {self.title}"

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=500)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    
    # We use index '0' for option_1 and '1' for option_2 to match your JS logic
    CORRECT_CHOICES = [
        ('0', 'Option 1'),
        ('1', 'Option 2'),
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    def __str__(self):
        return f"Q for {self.lesson.title}: {self.question_text[:30]}..."


class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Step(models.Model):
    THEORY = "theory"
    PRACTICE = "practice"
    QUIZ = "quiz"

    STEP_TYPE_CHOICES = [
        (THEORY, "Theory"),
        (PRACTICE, "Practice"),
        (QUIZ, "Quiz"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField(max_length=200)
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES, default=THEORY)
    content = models.TextField(blank=True, help_text="Theory or instruction content (HTML allowed)")
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.topic.title} - {self.title} ({self.step_type})"


class PracticeTask(models.Model):
    step = models.OneToOneField(Step, on_delete=models.CASCADE, related_name="practice_task")
    instruction = models.TextField()
    starter_content = models.TextField(blank=True)
    success_message = models.CharField(max_length=255, default="Great work. All checks passed.")

    def __str__(self):
        return f"Practice task for {self.step.title}"


class ValidationRule(models.Model):
    CONTAINS_TEXT = "contains_text"
    BOLD_TEXT = "bold_text"

    RULE_TYPE_CHOICES = [
        (CONTAINS_TEXT, "Contains Text"),
        (BOLD_TEXT, "Bold Text"),
    ]

    practice_task = models.ForeignKey(PracticeTask, on_delete=models.CASCADE, related_name="rules")
    name = models.CharField(max_length=120, help_text="Human-friendly test label")
    rule_type = models.CharField(max_length=30, choices=RULE_TYPE_CHOICES, default=CONTAINS_TEXT)
    expected_value = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.practice_task.step.title} - {self.name}"


class UserStepProgress(models.Model):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    PASSED = "passed"

    STATUS_CHOICES = [
        (LOCKED, "Locked"),
        (UNLOCKED, "Unlocked"),
        (PASSED, "Passed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="step_progress")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="user_progress")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=LOCKED)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "step")

    def __str__(self):
        return f"{self.user} - {self.step} - {self.status}"


class PracticeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="practice_submissions")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="submissions")
    submitted_content = models.TextField()
    is_passed = models.BooleanField(default=False)
    result_snapshot = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.step} - {'passed' if self.is_passed else 'failed'}"
