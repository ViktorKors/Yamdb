# from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Titles, Genre, Category
from rest_framework.pagination import LimitOffsetPagination
from .serializers import TitlesSerializer, GenreSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # 
    filterset_fields = ('year', 'name')
    search_fields = ('genre__slug', 'category__slug') 


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination

    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination