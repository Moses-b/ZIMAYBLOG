from django.contrib import admin

from .models import ContactLead


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "source", "created_at")
    search_fields = ("name", "email", "service", "message")
    list_filter = ("service", "source", "created_at")
