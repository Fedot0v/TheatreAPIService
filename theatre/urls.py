from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TicketModelViewSet
)

router = routers.DefaultRouter()

router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)
router.register("tickets", TicketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "theatre"
