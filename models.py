from django.db import models

class Agency(models.Model):
    """
    Business Layer: The SaaS Client Profile (inside the tenant schema).
    Holds operational metadata for the specific Client schema.
    """
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, blank=True)
    country_code = models.CharField(max_length=2, default='PT')
    default_currency = models.CharField(max_length=3, default='EUR')

    def __str__(self):
        return self.name

class Company(models.Model):
    """B2B Entity: The Corporate Renter."""
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    industry = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    """Identity Root: The Person (Epic 1.1)."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # KYC & PII Fields
    fiscal_id = models.CharField(max_length=50, blank=True, null=True) # NIF/NIE
    id_number = models.CharField(max_length=50, blank=True, null=True, unique=True) # Epic 1.2 Collision
    id_expiry_date = models.DateField(blank=True, null=True)
    kyc_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('verified', 'Verified')],
        default='pending'
    )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"