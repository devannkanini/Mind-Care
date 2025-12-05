from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms import IssueForm, HelpRequestForm
from .models import Issue, RequestHelp, ProfessionalHelp  



# Dashboard - requires login
@login_required
def dashboard(request):
    return render(request, 'mindCare/dashboard.html')

# Home page
def home(request):
    return render(request, 'mindCare/home.html')

# Login page
def loginUser(request):
    return render(request, 'mindCare/login_form.html')

# Register page
def registerUser(request):
    return render(request, 'mindCare/register_form.html')

# Logout
def logoutUser(request):
    logout(request)
    return redirect('home') 

# Professional Help page
@login_required
def professional_help(request):
    # Example data - later you can pull from DB
    professionals = [
        {"name": "Dr. Jane Mwangi", "specialty": "Psychologist", "email": "jane@example.com", "phone": "0741234567"},
        {"name": "Dr. John Kimani", "specialty": "Counselor", "email": "john@example.com", "phone": "0749876543"},
        {"name": "Dr. Aisha Hassan", "specialty": "Therapist", "email": "aisha@example.com", "phone": "0712345678"},
    ]
    return render(request, 'mindCare/professional_help.html', {"professionals": professionals})

def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your issue has been submitted successfully!")
            return redirect('mindCare:fetch_issues')
  
    else:
        form = IssueForm()
    return render(request, 'mindCare/form.html', context={'form': form})
def fetch_issues(request):
    
    return render(request, 'mindCare/issues.html')

def professional_help(request):
    professionals = ProfessionalHelp.objects.all()
    return render(request, 'mindCare/professional_help.html', {'professionals': professionals})


@login_required
def request_help(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help_request = form.save(commit=False)
            help_request.user = request.user  # link request to logged-in user
            help_request.save()
            messages.success(request, "Your help request has been sent! A professional will reach out.")
            return redirect('mindCare:request_help')  # redirect to same page or a "list" page
    else:
        form = HelpRequestForm()
    
    return render(request, 'mindCare/request_help.html', {'form': form})