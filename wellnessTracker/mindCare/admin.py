from django.contrib import admin
from .models import Issue, ProfessionalHelp, HelpRequest
from .models import Journal 
from .models import Booking


# Register your models here.
admin.site.register(Issue)
admin.site.register(ProfessionalHelp)
admin.site.register(HelpRequest)
admin.site.register(Journal)
admin.site.register(Booking)
