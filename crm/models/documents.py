from django.db import models
from crm.models.contact import Contact

class ContactDocument(models.Model):
    """Stores KYC and Onboarding documents linked to a Contact."""
    
    DOC_TYPES = [
        ('passport', 'Passport'),
        ('national_id', 'National ID'),
        ('nif_document', 'NIF / Tax ID'),
        ('bank_statement', 'Bank Statement'),
        ('lease_statement', 'Lease Statement'),
        ('driving_licence', 'Driving Licence'),
        ('other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=50, choices=DOC_TYPES, default='other')
    file = models.FileField(upload_to='kyc_docs/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.contact.first_name}"