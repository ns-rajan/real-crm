from rest_framework import viewsets
from .models import Article, LocalityNode, ScrapedListing
from .serializers import ArticleSerializer, LocalityNodeSerializer, ScrapedListingSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'


class LocalityNodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LocalityNode.objects.all()
    serializer_class = LocalityNodeSerializer


class ScrapedListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScrapedListing.objects.filter(
        visibility_level='public'
    ).select_related('locality')
    serializer_class = ScrapedListingSerializer