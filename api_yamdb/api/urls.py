# urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet, GenreViewSet, CategoryViewSet


router = DefaultRouter()

router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]