from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, LocalityNodeViewSet, ScrapedListingViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'districts', LocalityNodeViewSet, basename='district')
router.register(r'listings', ScrapedListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),
]