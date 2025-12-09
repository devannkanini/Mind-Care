from django.forms import ModelForm
from django import forms
from .models import Issue, HelpRequest, Booking
from .models import MoodLog 



class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', ]
 
class HelpRequestForm(forms.ModelForm):
    
    class Meta:
        model = HelpRequest
        fields = ['message'] 
        
        
        from django import forms
from .models import ProfessionalHelp

class ProfessionalHelpForm(forms.ModelForm):
    class Meta:
        model = ProfessionalHelp
        fields = ['title', 'description', 'availability', 'location', 'price', 'contact']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pediatrician / Counsellor'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe service...'}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mon-Fri 9am-5pm'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Clinic name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 1500.00'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone or email'}),
        }




class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'session_type', 'phone_number', 'description']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
class MoodLogForm(forms.ModelForm):

    level = forms.IntegerField(
        min_value=1,
        max_value=10,
        label="Intensity Level (1-10)",
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10})
    )
    
    class Meta:
        model = MoodLog
        fields = ['mood', 'level']