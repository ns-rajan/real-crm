from rest_framework import serializers
from .models import Article, LocalityNode, ScrapedListing

class LocalityNodeSerializer(serializers.ModelSerializer):
    overall_score = serializers.FloatField(source='overall_locality_score', read_only=True)

    class Meta:
        model = LocalityNode
        fields = ['id', 'name', 'description', 'score_accessibility', 'score_lifestyle', 'score_commercial', 'overall_score']

class ScrapedListingSerializer(serializers.ModelSerializer):
    locality_name = serializers.CharField(source='locality.name', read_only=True)
    freshness_label = serializers.CharField(source='get_data_freshness_tier_display', read_only=True)

    class Meta:
        model = ScrapedListing
        fields = [
            'id', 'title', 'source_platform', 'locality_name', 'address', 
            'estimated_price', 'currency', 'size_sqm', 'freshness_label', 
            'risk_flags', 'last_scraped_at'
        ]

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'excerpt', 'content', 'seo_title', 'seo_description', 'published_at']