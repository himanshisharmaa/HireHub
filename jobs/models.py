from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Job(models.Model):
    title=models.CharField( max_length=200)
    company=models.CharField( max_length=200)
    description=models.TextField()
    location= models.CharField( max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    employer=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'pk': self.pk})


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        VIEWED = 'Viewed', 'Viewed'
        SHORTLISTED = 'Shortlisted', 'Shortlisted'
        REJECTED = 'Rejected', 'Rejected' 
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    candidate=models.ForeignKey(User,on_delete=models.CASCADE)
    cover_letter=models.TextField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(
    max_length=50,
    choices=Status.choices,
    default='Pending')

    applied_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('job','candidate')
        
    def __str__(self):
        return f'{self.candidate.username} applied to {self.job.title}'
