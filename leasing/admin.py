from django.contrib import admin
from .models import Lead, Reservation, Lease

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("contact", "stage", "source", "stage_updated_at")
    list_filter = ("stage", "source")
    search_fields = ("contact__first_name", "contact__last_name", "contact__email")
    # Allows you to easily move leads through the Kanban stages right from the list view
    list_editable = ("stage",) 

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("unit", "lead", "start_date", "end_date", "expiry_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("lead__contact__first_name", "lead__contact__last_name", "unit__name")

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ("unit", "contact", "start_date", "end_date", "status", "monthly_rent")
    # This allows you to quickly change a lease status without opening the record
    list_editable = ("status",) 
    list_filter = ("status", "start_date")
    search_fields = ("contact__first_name", "contact__last_name", "unit__name")