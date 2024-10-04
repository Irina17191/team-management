from rest_framework import viewsets

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from teams.models import Team, Person
from teams.serializers import TeamSerializer, PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing persons.

    Provides CRUD operations for Person objects, including
    listing, creating, retrieving, updating, and deleting
    persons.
    """
    queryset = Person.objects.prefetch_related("teams").all()
    serializer_class = PersonSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams.

    Provides CRUD operations for Team objects, including
    listing, creating, retrieving, updating, and deleting
    teams. Supports filtering by team name.
    """
    queryset = Team.objects.prefetch_related("persons").all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset based on the 'name' query parameter.

        If the 'name' parameter is provided in the request,
        the queryset will be filtered to include only teams
        with names that contain the specified value.
        """
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
