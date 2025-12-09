from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import ProfessionalHelp, Booking
from django import forms
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import MoodLog 
from .forms import MoodLogForm, BookingForm
from .models import Booking # Make sure you import Booking






from .forms import IssueForm, HelpRequestForm, ProfessionalHelpForm
from .models import ProfessionalHelp, Booking, MoodLog, HelpRequest 
from .models import MoodLog,  JournalEntry 
from .models import MoodLog, JournalEntry
from .models import ProfessionalHelp
from .models import Journal








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
    return redirect('/mindCare/home') 

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
def request_help(request, id): 
    
    professional = get_object_or_404(ProfessionalHelp, id=id)

    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            helpRequest = form.save(commit=False)
            helpRequest.user = request.user 
            helpRequest.professional = professional
            helpRequest.save()
            
            messages.success(request, f"Your request for help from {professional.name} has been sent! They will reach out.")
            return redirect('mindCare:dashboard') 
    else:
        form = HelpRequestForm(initial={'professional': professional}) 
        
    context = {
        'form': form,
        'professional': professional
    }
    
    return render(request, 'mindCare/dashboard.html', context)

cl = MpesaClient()
        # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
        # phone_number = '0717817826'
        # amount = 1
        # account_reference = 'reference'
        # transaction_desc = 'Description'
        # callback_url = 'https://api.darajambili.com/express-payment'
        # response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        # return HttpResponse(response)

@login_required
def mpesaPayment(request, booking_id):
    

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)


    if booking.payment_status == 'completed':
        
        return redirect('mindCare:booking_detail', id=booking.id) 

    if request.method == 'POST':

        phoneNumber = booking.phone_number 
        amount = int(booking.amount) 
        cl = MpesaClient()
        accountReference = f'BOOKING_{booking.id}' 
        transactionDesc = f'Payment for session with {booking.professional.title}'
    
        callbackUrl = 'YOUR_SAFARICOM_VALIDATED_CALLBACK_URL' 

        try:
            
            response = cl.stk_push(phoneNumber, amount, accountReference, transactionDesc, callbackUrl)
            
            checkout_request_id = response.get('CheckoutRequestID')
            
            if checkout_request_id:
                booking.checkout_request_id = checkout_request_id
                booking.payment_status = 'pending'
                booking.save()
                

                return redirect('mindCare:booking_detail', id=booking.id)
            else:
                
                error_message = response.get('CustomerMessage', 'Payment initiation failed.')
                return render(request, 'mindCare/mpesa_payments.html', {"error": error_message, "booking": booking})

        except Exception as e:
        
            return render(request, 'mindCare/mpesa_payments.html', {"error": f"An error occurred: {e}", "booking": booking})



    context = {
        'booking': booking,
        'professional': booking.professional
    }
    return render(request, 'mindCare/mpesa_payments.html', context)
@login_required
@login_required
def logJournal(request):
    
    
    if request.method == "POST":

        content = request.POST.get('content')
        
        if content:
        
            Journal.objects.create( user=request.user,content=content)
            messages.success(request, "Journal entry saved successfully!")
            return redirect('mindCare:journal') 
        else:
            messages.error(request, "Journal content cannot be empty.")
            
    journals = Journal.objects.filter(user=request.user).order_by('-date_created')
    
    context = { 'journals': journals}
    return render(request, 'mindCare/journal.html', context)

def journal_detail(request, pk):

    journal = get_object_or_404(Journal, pk=pk, user=request.user)
    context = {'journal': journal}
    return render(request, 'mindCare/journal_detail.html', context)


@login_required
def delete_journal(request, id):
    """Delete a journal entry with confirmation"""
    

    journal = get_object_or_404(Journal, id=id, )
    
    
    if request.method == 'POST':
        journal.delete()
        messages.success(request, 'Journal entry deleted successfully.')
    
        return redirect('mindCare:journal')

    context = {'journal': journal}
    return render(request, 'mindCare/delete_journal.html', context)


@login_required
def dashboard(request):
    # Get user-specific data
    moods = MoodLog.objects.filter(user=request.user).order_by('-created_at')[:7]  # last 7 moods
    journals = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:5]  # last 5 journals
    help_requests = HelpRequest.objects.filter(user=request.user)

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
        
        return redirect('mindCare:dashboard')
    else:
        
        return redirect('mindCare:registerUser')
    
    

@login_required
def book_professional(request, id):
    professional = get_object_or_404(ProfessionalHelp, id=id, is_paid=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            
            booking = form.save(commit=False)
            
            
            booking.user = request.user
            booking.professional = professional
            
            
            booking.amount = professional.price 

            booking.save()
            
            return redirect('mindCare:mpesaPayment', booking_id=booking.id)
            
    else:

        form = BookingForm()

    context = {
        'professional': professional,
        'form': form,
    }
    return render(request, 'mindCare/booking_form.html', context)


@login_required
def booking_detail(request, id):
    # Retrieve the booking securely
    booking = get_object_or_404(Booking, id=id, user=request.user)
    
    context = {
        'booking': booking
    }
    return render(request, 'mindCare/booking_detail.html', context)

@login_required
def my_bookings(request):
    # Retrieve all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('booking_date', 'booking_time')
    
    context = {
        'upcoming_bookings': bookings.filter(booking_status='confirmed').filter(
            Q(booking_date__gt=timezone.localdate()) | 
            Q(booking_date=timezone.localdate(), booking_time__gt=timezone.localtime().time())
        ),
        'history_bookings': bookings.exclude(booking_status='confirmed').order_by('-booking_date'),
        'pending_bookings': bookings.filter(payment_status='pending'),
    }
    
    return render(request, 'mindCare/my_bookings.html', context)

@login_required
def logMood(request):
    
     if request.method == 'POST':
         form = MoodLogForm(request.POST)
        
         if form.is_valid():
            # Create object but don't save yet (commit=False)
            mood_entry = form.save(commit=False)
            
            # Assign the current user (security critical step)
            mood_entry.user = request.user
            
            # Save the object to the database
            mood_entry.save()
            
            messages.success(request, 'Mood logged successfully!')
            return redirect('mindCare:mood') 
         else:
            messages.error(request, 'There was an error in your submission.')
        
     form = MoodLogForm()
    

     mood_history = MoodLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    
     context = {
        'form': form,
        'mood_history': mood_history
    }
    
     return render(request, 'mindCare/mood.html', context)
@login_required
def my_help_requests(request):
    """Fetches and displays all help requests made by the current user."""
    
    # Query all requests linked to the logged-in user
    requests = HelpRequest.objects.filter(user=request.user).order_by('-date_requested')
    
    context = {
        'requests': requests
    }
    
    return render(request, 'mindCare/my_help_requests.html', context)
