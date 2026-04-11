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
