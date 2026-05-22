from django.contrib import admin
from .models import MacroInsight, LocalityNode, ScrapedListing, Article

admin.site.register(MacroInsight)

@admin.register(LocalityNode)
class LocalityNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'score_accessibility', 'score_lifestyle', 'score_commercial', 'overall_locality_score')
    search_fields = ('name',)

@admin.register(ScrapedListing)
class ScrapedListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'locality', 'estimated_price', 'currency', 'visibility_level', 'last_scraped_at')
    list_filter = ('visibility_level', 'data_freshness_tier', 'currency', 'locality')
    search_fields = ('title', 'address', 'source_url')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'category', 'excerpt', 'content')}),
        ('SEO Metadata', {'classes': ('collapse',), 'fields': ('seo_title', 'seo_description')}),
        ('Publishing', {'fields': ('status', 'published_at')}),
    )