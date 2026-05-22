from django.db import models
from django.utils import timezone

class MacroInsight(models.Model):
    region = models.CharField(max_length=255, default="Lisbon")
    metric_name = models.CharField(max_length=255)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    metric_unit = models.CharField(max_length=50)
    source = models.CharField(max_length=255)
    recorded_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.region} - {self.metric_name}"

class LocalityNode(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    score_accessibility = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    score_lifestyle = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    score_commercial = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    @property
    def overall_locality_score(self):
        return round((float(self.score_accessibility) + float(self.score_lifestyle) + float(self.score_commercial)) / 3, 1)

    def __str__(self):
        return self.name

class ScrapedListing(models.Model):
    TIER_1, TIER_2, TIER_3 = 'TIER_1', 'TIER_2', 'TIER_3'
    DATA_FRESHNESS_CHOICES = [
        (TIER_1, 'Tier 1 (Green) - Live API/Verified'),
        (TIER_2, 'Tier 2 (Yellow) - Scraped < 30 Days'),
        (TIER_3, 'Tier 3 (Grey) - Scraped > 45 Days'),
    ]

    VISIBILITY_PUBLIC, VISIBILITY_MARKETPLACE, VISIBILITY_PRIVATE = 'public', 'marketplace', 'private'
    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, 'Public'),
        (VISIBILITY_MARKETPLACE, 'Marketplace'),
        (VISIBILITY_PRIVATE, 'Private'),
    ]

    title = models.CharField(max_length=255)
    source_url = models.URLField(unique=True, max_length=500)
    source_platform = models.CharField(max_length=255)
    locality = models.ForeignKey(LocalityNode, on_delete=models.SET_NULL, null=True, related_name='listings')
    address = models.CharField(max_length=255)
    estimated_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='EUR')
    size_sqm = models.IntegerField(null=True, blank=True)
    data_freshness_tier = models.CharField(max_length=20, choices=DATA_FRESHNESS_CHOICES, default=TIER_2)
    risk_flags = models.JSONField(default=list, blank=True)
    visibility_level = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_PUBLIC)
    last_scraped_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_data_freshness_tier_display()}] {self.title}"

class Article(models.Model):
    CATEGORY_CHOICES = [('market', 'Market Intelligence'), ('guides', 'Neighbourhood Guides'), ('explained', 'CRE Explained')]
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, help_text="URL friendly title (e.g., lisbon-q2-report)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='market')
    excerpt = models.TextField(blank=True, help_text="Short summary for the homepage card.")
    content = models.TextField(help_text="Paste your Google Doc content here. HTML is supported.")
    seo_title = models.CharField(max_length=255, blank=True, help_text="Overrides title for search engines if provided.")
    seo_description = models.TextField(blank=True, help_text="Meta description for Google.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"