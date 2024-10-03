from rest_framework import viewsets
from teams.models import Team, Person
from teams.serializers import TeamSerializer, PersonSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related("teams").all()
    serializer_class = PersonSerializer
