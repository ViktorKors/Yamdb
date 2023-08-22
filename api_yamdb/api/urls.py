from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet


router = DefaultRouter()

router.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]