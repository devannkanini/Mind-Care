from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.models import User






from .forms import IssueForm, HelpRequestForm, ProfessionalHelpForm
from .models import Issue, RequestHelp, ProfessionalHelp 
from .models import MoodLog, RequestHelp, JournalEntry 
from .models import MoodLog, JournalEntry
from .models import ProfessionalHelp





# Dashboard - requires login
@login_required
def dashboard(request):
    return render(request, 'mindCare/dashboard.html')

# Home page
def home(request):
    return render(request, 'mindCare/home.html')

# Login page
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mindCare:dashboard')   
        else:
            return render(request, 'mindCare/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'mindCare/login.html')


# Register page
def registerUser(request):
    return render(request, 'mindCare/register_form.html')

# Logout
def logoutUser(request):
    logout(request)
    return redirect('home') 

# # Professional Help page
# # @login_required
# def professionalHelp(request):
#     # Example data - later you can pull from DB
#     professionals = [
#         {"name": "Dr. Jane Mwangi", "specialty": "Psychologist", "email": "jane@example.com", "phone": "0741234567"},
#         {"name": "Dr. John Kimani", "specialty": "Counselor", "email": "john@example.com", "phone": "0749876543"},
#         {"name": "Dr. Aisha Hassan", "specialty": "Therapist", "email": "aisha@example.com", "phone": "0712345678"},
#     ]
#     return render(request, 'mindCare/professional_help.html', {"professionals": professionals})

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

def help_list(request):
    professionals = ProfessionalHelp.objects.all()
    context={'professionals': professionals}
    return render(request, 'mindCare/professional_help.html', context)

@login_required
def requestHelp(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            helpRequest = form.save(commit=False)
            helpRequest.user = request.user  # link request to logged-in user
            helpRequest.save()
            messages.success(request, "Your help request has been sent! A professional will reach out.")
            return redirect('mindCare:requestHelp')  # redirect to same page or a "list" page
    else:
        form = HelpRequestForm()
    
    return render(request, 'mindCare/requestHelp.html', {'form': form})
def index(request):

        cl = MpesaClient()
        # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
        # phone_number = '0717817826'
        # amount = 1
        # account_reference = 'reference'
        # transaction_desc = 'Description'
        # callback_url = 'https://api.darajambili.com/express-payment'
        # response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        # return HttpResponse(response)

def mpesaPayment(request):
    if request.method == 'POST':
        phoneNumber = request.POST.get('phoneNumber')
        amount = int(request.POST.get('amount'))

        cl = MpesaClient()
        accountReference = 'Professional Help'
        transactionDesc = 'payment for professional help'
        callbackUrl = 'https://api.darajambili.com/express-payment'

        response = cl.stk_push(phoneNumber, amount, accountReference, transactionDesc, callbackUrl)

        return render(request, 'mindCare/mpesa_payments.html', {"response": response})

    # GET request → just load the page, don’t use phoneNumber
    return render(request, 'mindCare/mpesa_payments.html')

@login_required
def user_dashboard(request):
    issues = Issue.objects.filter(user=request.user) if hasattr(Issue, 'user') else Issue.objects.all()
    help_requests = RequestHelp.objects.filter(user=request.user)
    
    context = {
        'issues': issues,
        'help_requests': help_requests,
    }
    return render(request, 'mindCare/dashboard.html', context)

@login_required
def logMood(request):
    if request.method == "POST":
        mood_value = request.POST.get('mood')
        MoodLog.objects.create(user=request.user, mood=mood_value)
        return redirect('mindCare:dashboard')
    return render(request, 'mindCare/mood.html')

@login_required
def logJournal(request):
    if request.method == "POST":
        content = request.POST.get('content')
        JournalEntry.objects.create(user=request.user, entry=content)  # <-- use 'entry'
        return redirect('mindCare:dashboard')
    return render(request, 'mindCare/journal.html')
@login_required
def fetch_issues(request):
    issues = Issue.objects.all()
    return render(request, 'mindCare/issues.html', {'issues': issues})

@login_required
def dashboard(request):
    # Get user-specific data
    moods = MoodLog.objects.filter(user=request.user).order_by('-created_at')[:7]  # last 7 moods
    journals = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:5]  # last 5 journals
    help_requests = RequestHelp.objects.filter(user=request.user)

    context = {
        'moods': moods,
        'journals': journals,
        'help_requests': help_requests,
    }
    return render(request, 'mindCare/dashboard.html', context)
    from django.contrib.auth.models import User

def registerUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("mindCare:registerUser")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("mindCare:registerUser")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully!")
        return redirect("mindCare:loginUser")

    return render(request, 'mindCare/register_form.html')


@login_required
def help_list(request):
    print(ProfessionalHelp)
    professionals = ProfessionalHelp.objects.all()
    return render(request, 'mindCare/professional_help.html', {'professionals': professionals})

@login_required
@login_required
def create_help(request):
    if request.method == "POST":
        form = ProfessionalHelpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mindCare:help_list')  # use the URL name, not the path
    else:
        form = ProfessionalHelpForm()

    return render(request, 'mindCare/create_help.html', {'form': form})

@login_required
def update_help(request, id):
    professional = ProfessionalHelp.objects.get(id=id)

    if request.method == "POST":
        professional.title = request.POST.get('title')
        professional.description = request.POST.get('description')
        professional.save()

        messages.success(request, "Updated successfully!")
        return redirect('mindCare:help_list')

    return render(request, 'mindCare/update_help.html', {'professional': professional})
@login_required
def delete_help(request, id):
    professional = ProfessionalHelp.objects.get(id=id)

    if request.method == "POST":
        professional.delete()
        messages.success(request, "Deleted successfully!")
        return redirect('mindCare:help_list')

    return render(request, 'mindCare/delete_help.html', {'professional': professional})
@login_required
def journal_detail(request, id):
    journal = JournalEntry.objects.get(id=id, user=request.user)
    return render(request, 'mindCare/journal_detail.html', {'journal': journal})

def about_us(request):
    return render(request, 'mindCare/about_us.html')

def get_started(request):
    if request.user.is_authenticated:
        # If user is logged in, go to dashboard
        return redirect('mindCare:dashboard')
    else:
        # If not logged in, go to register page
        return redirect('mindCare:registerUser')

