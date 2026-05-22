from rest_framework import serializers
from .models import Article, LocalityNode, ScrapedListing


class LocalityNodeSerializer(serializers.ModelSerializer):
    overall_score = serializers.FloatField(source='overall_locality_score', read_only=True)

    class Meta:
        model = LocalityNode
        fields = [
            'id', 'name', 'description', 
            'score_accessibility', 'score_lifestyle', 'score_commercial', 
            'overall_score'
        ]


class ScrapedListingSerializer(serializers.ModelSerializer):
    locality_name = serializers.CharField(source='locality.name', read_only=True)
    data_freshness_tier_display = serializers.CharField(source='get_data_freshness_tier_display', read_only=True)

    class Meta:
        model = ScrapedListing
        fields = [
            'id', 'title', 'source_url', 'source_platform', 'locality', 
            'locality_name', 'address', 'estimated_price', 'currency', 
            'size_sqm', 'data_freshness_tier', 'data_freshness_tier_display', 
            'risk_flags', 'visibility_level', 'last_scraped_at'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'category', 'excerpt', 'content', 
            'seo_title', 'seo_description', 'status', 'published_at', 
            'created_at', 'updated_at'
        ]