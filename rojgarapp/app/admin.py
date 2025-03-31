from django.contrib import admin
from app.models import UserDetails, PersonalDetails, Professions

# Register your models here.

admin.site.register(UserDetails)
admin.site.register(PersonalDetails)
admin.site.register(Professions)
admin.site.register(JobAnnouncement)
