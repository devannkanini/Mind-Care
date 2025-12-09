from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




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
    is_professional = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class HelpRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey('ProfessionalHelp', on_delete=models.CASCADE) 
    message = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('contacted', 'Contacted by Professional'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Request by {self.user.username} for {self.professional.title}"

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
    


class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending_payment', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    SESSION_TYPE = [
        ('individual', 'Individual Session'),
        ('couple', 'Couple Session'),
        ('family', 'Family Session'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(ProfessionalHelp, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE, default='individual')
    description = models.TextField(blank=True)
    
    # Payment details
    phone_number = models.CharField(max_length=12)  # Format: 254XXXXXXXXX
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending_payment')
    
    # M-Pesa details
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_created']
        unique_together = ['professional', 'booking_date', 'booking_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.professional.name} on {self.booking_date}"
    
    def is_upcoming(self):
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(self.booking_date, self.booking_time)
        )
        return booking_datetime > timezone.now()
    


class Journal(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200) 
    content = models.TextField() 
    date_created = models.DateTimeField(auto_now_add=True) 
    mood_rating = models.IntegerField(default=5) 

    def __str__(self):
        return f'{self.title} by {self.user.username}'

    class Meta:
        ordering = ['-date_created'] 