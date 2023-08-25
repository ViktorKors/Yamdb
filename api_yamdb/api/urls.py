from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet, GenreViewSet, ReviewsViewSet, CommentViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r"titles", TitlesViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentViewSet, basename="comments")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")


urlpatterns = [
    path("v1/", include(router.urls)), 
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
]
