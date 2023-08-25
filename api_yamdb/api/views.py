from rest_framework import viewsets, filters
from reviews.models import Review, Comment, Titles, Genre, Category
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ReviewSerializer, CommentSerializer, TitlesSerializer, GenreSerializer, CategorySerializer
from .permissions import AdminOrModeratorOrReadOnly, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter) 
    filterset_fields = ("year", "name")
    search_fields = ("genre__slug", "category__slug") 
    
    
class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)
        return title.reviews.all()
      
      
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

