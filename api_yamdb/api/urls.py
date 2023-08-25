from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet, ReviewsViewSet, CommentViewSet, GenreViewSet

router = DefaultRouter()

router.register(r"titles", TitlesViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)

router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentViewSet, basename="comments")
router.register(r"genres", GenreViewSet, basename="genres")

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
