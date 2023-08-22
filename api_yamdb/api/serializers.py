from reviews.models import Titles, Genre, Category, GenreTitles
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    # name = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Genre.objects.all(),
    # )
    genre_name = serializers.CharField(source='name')
    genre_slug = serializers.CharField(source='slug')

    class Meta:
        fields = ('id', 'genre_name', 'genre_slug')
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    # genre = GenreSerializer(many=True, required=False)
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            titles = Titles.objects.create(**validated_data)
            return titles
        else:
            genres = validated_data.pop('genre')
            print(genres)
            titles = Titles.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    name = genre  )  #  **genre
                GenreTitles.objects.create(
                    genre=current_genre, titles=titles)
            return titles


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category