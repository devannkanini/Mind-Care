from django.urls import path
from . import views

app_name = 'mindCare'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.registerUser, name='registerUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('dashboard/', views.dashboard, name='dashboard'),  

    # PROFESSIONAL HELP CRUD
    path('professional-help/', views.help_list, name='help_list'),
    path('professional-help/create/', views.create_help, name='create_help'),
    path('professional-help/update/<int:id>/', views.update_help, name='update_help'),
    path('professional-help/delete/<int:id>/', views.delete_help, name='delete_help'),

    # path('create-issue/', views.create_issue, name='create_issue'),
    path('issue/', views.fetch_issues, name='fetch_issues'),
    path('request-help/<int:id>/', views.request_help, name='request_help'),
    path('mpesaPayment/<int:booking_id>/', views.mpesaPayment, name='mpesaPayment'),
    path('mood/', views.logMood, name='mood'),
    path('journal/', views.logJournal, name='journal'),
    path('journal/<int:id>/', views.journal_detail, name='journal_detail'),
    path('about/', views.about_us, name='about_us'), 
    path('get started/', views.get_started, name='get_started'),
    path('journal/delete/<int:id>/', views.delete_journal, name='delete_journal'), 
    path('professional-help/book/<int:id>/', views.book_professional, name='book_professional'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-help-requests/', views.my_help_requests, name='my_help_requests'),
    path('professional/dashboard/', views.professional_dashboard, name='pro_dashboard'),


]
