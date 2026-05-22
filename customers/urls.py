from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, LocalityNodeViewSet, ScrapedListingViewSet

router = DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'district', LocalityNodeViewSet, basename='district')
router.register(r'listing', ScrapedListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),
]