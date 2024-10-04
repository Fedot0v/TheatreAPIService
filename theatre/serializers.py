from rest_framework import serializers

from theatre.models import Actor, Genre, Play


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class ActorDetailSerializer(ActorSerializer):
    movies = PlaySerializer(many=True, read_only=True)

    class Meta(ActorSerializer.Meta):
        fields = ActorSerializer.Meta.fields + ("movies",)


class GenreDetailSerializer(GenreSerializer):
    movies = PlaySerializer(many=True, read_only=True)

    class Meta(GenreSerializer.Meta):
        fields = GenreSerializer.Meta.fields + ("movies",)


