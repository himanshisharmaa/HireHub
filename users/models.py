from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_employer=models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # 🆕 Added here
    def __str__(self):
        return f'{self.user.username} Profile'
    
# @receiver(post_save,sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     instance.profile.save()