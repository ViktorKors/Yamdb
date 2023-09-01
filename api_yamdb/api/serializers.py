import re

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title, User


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""

    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review."""

    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )

    def validate(self, data):
        """
        Function that checks that one user cannot submit multiple reviews.
        """
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError("Only one review is allowed")
        return data

    class Meta:
        fields = ("id", "author", "title", "text", "pub_date", "score")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("review",)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ProfileEditSerializer(UserSerializer):
    """Serializer for Profile."""

    role = serializers.CharField(read_only=True)


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Registration."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self):
        """Function to save a user."""
        result = re.search(r"^[\w.@+-]", self.validated_data["username"])
        if not result:
            raise serializers.ValidationError("Come up with another nickname")

        user, self.create = User.objects.get_or_create(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        return user

    def validate_username(self, value):
        """Function that checks the username range boundaries."""
        if value.lower() == "me":
            raise serializers.ValidationError(
                f"Using name {value}" f"as username is not allowed"
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Serializer for Token."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Serializer for ReadOnlyTitle."""

    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )
