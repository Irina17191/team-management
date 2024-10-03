from rest_framework import serializers
from teams.models import Team, Person


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")


class PersonSerializer(serializers.ModelSerializer):
    teams = serializers.PrimaryKeyRelatedField(many=True, queryset=Team.objects.all())

    class Meta:
        model = Person
        fields = ("id", "name", "last_name", "email", "teams")
