from rest_framework import viewsets

from cinema.models import (CinemaHall,
                           Genre,
                           Actor,
                           Movie,
                           MovieSession
                           )
from cinema.serializers import (CinemaHallSerializer,
                                GenreSerializer,
                                ActorSerializer,
                                MovieSerializer,
                                MovieSessionSerializer,
                                MovieSessionListSerializer,
                                MovieListSerializer,
                                MovieCreateSerializer
                                )


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related("actors", "genres")

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return MovieCreateSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.prefetch_related()
        return queryset


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.select_related("movie", "cinema_hall")

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        return MovieSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset
