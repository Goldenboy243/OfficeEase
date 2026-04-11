from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Profile({self.user.username})"


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

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