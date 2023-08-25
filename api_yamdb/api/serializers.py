from rest_framework import serializers
from reviews.models import Review, Comment, User, Genre, Titles, Category, GenreTitles
from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
