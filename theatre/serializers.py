from django.db import transaction
from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "image")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres", "image")


class ActorDetailSerializer(ActorSerializer):
    movies = PlaySerializer(many=True, read_only=True)

    class Meta(ActorSerializer.Meta):
        fields = ActorSerializer.Meta.fields + ("movies",)


class ActorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "image")


class GenreDetailSerializer(GenreSerializer):
    movies = PlaySerializer(many=True, read_only=True)

    class Meta(GenreSerializer.Meta):
        fields = GenreSerializer.Meta.fields + ("movies",)


class PlayListSerializer(PlaySerializer):
    class Meta(PlaySerializer.Meta):
        fields = ("id", "title")


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    """We define a field to get the number of free seats through the serializer method"""
    available_seats_count = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = PerformanceSerializer.Meta.fields + ("available_seats_count",)

    """We call the get_free_seats_count() method of the Performance model to get it
    of free places for the current object (obj) """
    def get_available_seats_count(self, obj):
        return len(obj.free_seats_count())


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")
        read_only_fields = ("created_at", "user")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket)
            return reservation

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")
        read_only_fields = ("reservation",)
