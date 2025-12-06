from django.urls import path
from . import views
app_name = 'mindCare'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.registerUser, name='registerUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('professional-help/', views.professionalHelp, name='professional_help'),
    path('create-issue/', views.create_issue, name='create_issue'),
    path('issue/', views.fetch_issues, name='fetch_issues'),
    path('request-help/', views.requestHelp, name='request_help'),
    path('mpesaPayment/', views.mpesaPayment, name='mpesaPayment   '),
    path('mood/', views.logMood, name='mood'),
    path('journal/', views.logJournal, name='journal'),


]
