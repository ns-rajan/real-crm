from django.db import models
from django.db.models import Q, CheckConstraint
from crm.models import Contact
from inventory.models import Unit

class Lead(models.Model):
    """Top of Funnel Pipeline (Epic 12.1)"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='leads')
    stage = models.CharField(
        max_length=30,
        choices=[
            ('new', 'New'), 
            ('contacted', 'Contacted'), 
            ('verification', 'KYC/Docs'), 
            ('negotiation', 'Negotiation'), 
            ('won', 'Won'), 
            ('lost', 'Lost')
        ],
        default='new'
    )
    stage_updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=50, default='manual') # Epic 11.1 Attribution
    
    # Epic 12.4: Many-to-Many Unit Binding
    interested_units = models.ManyToManyField(Unit, related_name='interested_leads', blank=True)

    def __str__(self):
        return f"Lead: {self.contact.first_name} {self.contact.last_name}"

class Reservation(models.Model):
    """Soft Hold Engine (Epic 3.2)"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='reservations')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    expiry_date = models.DateTimeField(null=True, blank=True) # Manual or Auto Release

    def __str__(self):
        return f"Hold: {self.unit.name} for {self.lead.contact.first_name}"

class Lease(models.Model):
    """Immutable Legal Contract (Epic 3.3)"""
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='leases') # The "Tenant"
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='leases')
    
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'), 
            ('signed', 'Signed'), 
            ('active', 'Active'), 
            ('superseded', 'Superseded'), # Epic 3.3 Immutability
            ('terminated', 'Terminated')
        ],
        default='draft'
    )
    class Meta:
        # Prevents impossible date ranges at the DB level
        constraints = [
            CheckConstraint(
                condition=Q(end_date__gte=models.F('start_date')),
                name='check_lease_dates_validity'
            )
        ]


    def __str__(self):
        return f"Lease: {self.unit.name} ({self.start_date} to {self.end_date})"