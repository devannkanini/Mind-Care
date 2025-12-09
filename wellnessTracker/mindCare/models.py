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
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

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



class MoodLog(models.Model):
     MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('anxious', 'Anxious'),
        ('stressed', 'Stressed'),
    ]
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
     level = models.IntegerField(default=5)  # 1-10 scale
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.level})"

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"