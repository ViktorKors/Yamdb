from reviews.models import Titles, Genre, Category, GenreTitles
from rest_framework import serializers
from datetime import datetime


class GenreSerializer(serializers.ModelSerializer):
    # name = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Genre.objects.all(),
    #     required=False,
    # )    

    class Meta:
        fields = ('name', 'slug')   #  
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        fields = '__all__'
        model = Titles

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Titles.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
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
                f'Год {data} больше текущего!',
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category