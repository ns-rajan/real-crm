from django.contrib import admin
from .models import Asset, Space, Unit

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("name", "asset")
    list_filter = ("asset",)
    search_fields = ("name", "asset__name")

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    # Updated to match our new PRD fields
    list_display = ("name", "space", "unit_type", "status", "visibility_level")
    
    # Make status and visibility instantly editable like a spreadsheet
    list_editable = ("status", "visibility_level") 
    
    # Powerful filtering for your Ops team
    list_filter = ("status", "visibility_level", "unit_type", "space__asset")
    search_fields = ("name", "space__name")