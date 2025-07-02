from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import UserDetails, PersonalDetails, Professions, JobAnnouncement, JobApplication, CustomUser
from django.utils.translation import gettext_lazy as _

# Register your models here.

admin.site.site_header = _("Rojgar App Admin")
admin.site.site_title = _("Rojgar App Admin Portal")
admin.site.index_title = _("Welcome to Rojgar App Admin Portal")


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "Email", "Gender", "PhoneNumber", "DOB", "Skill", "Address")
    list_filter = ("Gender", "DOB")
    search_fields = ("name", "Email", "PhoneNumber", "Skill")


class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email_address", "mobile_number", "gender", "dob", "status", "employment_status", "created_at")
    list_filter = ("gender", "status", "employment_status", "education_background", "created_at")
    search_fields = ("first_name", "last_name", "email_address", "mobile_number", "citizenship_number")
    readonly_fields = ("created_at",)


class ProfessionsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class JobAnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "profession", "posted_by", "required_personnel", "is_active", "posted_date")
    list_filter = ("is_active", "posted_date", "profession")
    search_fields = ("title", "description", "posted_by__username")
    readonly_fields = ("posted_date",)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "applicant", "status", "application_date")
    list_filter = ("status", "application_date")
    search_fields = ("job__title", "applicant__first_name", "applicant__last_name")
    readonly_fields = ("application_date",)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    ordering = ('phone_number',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)
admin.site.register(Professions, ProfessionsAdmin)
admin.site.register(JobAnnouncement, JobAnnouncementAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
