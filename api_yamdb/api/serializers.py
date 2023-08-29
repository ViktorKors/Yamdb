from django.shortcuts import get_object_or_404

from rest_framework import serializers
<<<<<<< HEAD
from reviews.models import Review, Comment, User, Genre, Titles, Category, GenreTitles
from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
=======
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title, User


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
>>>>>>> 94d53569c1c5fbd96b8de5f2fa96a35d32ee361b
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
        fields = ("id", "author", "title", "text", "pub_date", "rating")
        model = Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("review",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = "__all__"
        
        
class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        fields = "__all__"
        model = Titles

    def create(self, validated_data):
        if "genre" not in self.initial_data:
            title = Titles.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop("genre")
            title = Titles.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                     **genre )
                GenreTitles.objects.create(
                    genre=current_genre, titles=title)
            return title

    def validate_year(self, data):
        if data >= datetime.now().year:
            raise serializers.ValidationError(
                f"Год {data} больше текущего!",
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "slug")
        model = Category
=======
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ProfileEditSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def save(self):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        user.save()
        return user

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                f"Использование имени {value} "
                f"в качестве username запрещено"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=100)


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source="reviews__rating__avg", read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
>>>>>>> 94d53569c1c5fbd96b8de5f2fa96a35d32ee361b
