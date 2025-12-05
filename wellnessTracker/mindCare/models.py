from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('anxiety', 'Anxiety'),
        ('stress', 'Stress'),
        ('depression', 'Depression'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
        
class ProfessionalHelp(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    price=models.FloatField()

    def __str__(self):
        return self.name
    
class RequestHelp(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        professional_name = models.CharField(max_length=200)
        issue_title = models.CharField(max_length=200)
        issue_description = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

        def __str__(self):
         return f"{self.user.username} - {self.professional_name}"