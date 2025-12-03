from django.db import models

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
    image = models.ImageField(upload_to='issues/', blank=True, null=True)

    def __str__(self):
        return self.title

# 🌿 Professional Help Model
class Professional(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    availability = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
