from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitlesFilter
from .permissions import AdminOrModeratorOrReadOnly, IsAdmin, IsAdminOrReadOnly, AuthorOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileEditSerializer,
                          ReadOnlyTitleSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins


class CreateDestroyListGenericViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()    
    http_method_names =  ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):        
        if request.method == "PATCH":
            serializer = ProfileEditSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([permissions.AllowAny])
def registration(request):
    data = {}
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data["email"] = user.email
    data["username"] = user.username
    code = default_token_generator.make_token(user)
    send_mail(
        subject="yamdb_registration",
        message=f"User {user.username} successful"
                f"registered."
                f"Confirmation code: {code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(data, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([permissions.AllowAny])
def verification(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = {}
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    code = serializer.validated_data["confirmation_code"]
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        data["token"] = str(token)
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CategoryViewSet(CreateDestroyListGenericViewSet):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    @action(
        detail=False, methods=["DELETE"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug"
    )
    def get_category(self, request, slug):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(CreateDestroyListGenericViewSet):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    @action(
        detail=False, methods=["DELETE"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug"
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
