from django.db import models

class Asset(models.Model):
    """Root Property (e.g., The Building)"""
    name = models.CharField(max_length=255)
    address = models.TextField()
    # Epic 8.1: Tier 3 Data
    locality_score = models.JSONField(blank=True, null=True, help_text="Stores Maps/Transit API data") 

    def __str__(self):
        return self.name
    
class Space(models.Model):
    """Zone or Floor within an Asset"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='spaces')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.asset.name} - {self.name}"

class Unit(models.Model):
    """The granular Rentable Entity"""
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100)
    
    unit_type = models.CharField(
        max_length=50,
        choices=[
            ('desk', 'Dedicated Desk'),
            ('private_office', 'Private Office'),
            ('meeting_room', 'Meeting Room'),
            ('virtual_office', 'Virtual Office')
        ]
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('maintenance', 'Maintenance'),
            ('offline', 'Offline')
        ],
        default='active',
        help_text="Physical status only. Occupancy is derived."
    ) # Epic 2.2: Physical Status ONLY
    
    # Epic 15: Listing Projection Control
    visibility_level = models.CharField(
        max_length=20,
        choices=[
            ('private', 'Private (Internal Only)'), 
            ('marketplace', 'Marketplace (Logged-in)'), 
            ('public', 'Public (Fully Indexed)')
        ],
        default='private'
    )

    def __str__(self):
        return f"{self.space.name} - {self.name}"