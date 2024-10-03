from rest_framework import viewsets

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from teams.models import Team, Person
from teams.serializers import TeamSerializer, PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related("teams").all()
    serializer_class = PersonSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related("persons").all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter team by name (ex. ?name=developer)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
