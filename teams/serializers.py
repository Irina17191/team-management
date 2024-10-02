from rest_framework import serializers
from teams.models import Team, Person


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")


class PersonSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)

    class Meta:
        model = Person
        fields = ("id", "name", "last_name", "email", "teams")

    # def create(self, validated_data):
    #     teams_data = validated_data.pop("teams")
    #     person = Person.objects.create(**validated_data)
    #     self._add_teams(person, teams_data)
    #     return person
    #
    # def update(self, instance, validated_data):
    #     teams_data = validated_data.pop("teams", None)
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.last_name = validated_data.get("last_name", instance.last_name)
    #     instance.email = validated_data.get("email", instance.email)
    #     instance.save()
    #
    #     if teams_data is not None:
    #         instance.teams.clear()
    #         self._add_teams(instance, teams_data)
    #
    #     return instance
    #
    # def _add_teams(self, person, teams_data):
    #     """Add teams to the person."""
    #     for team_data in teams_data:
    #         # Validation: Check if the 'name' field exists
    #         if "name" not in team_data:
    #             raise serializers.ValidationError("Team name is required.")
    #
    #         try:
    #             team, created = Team.objects.get_or_create(**team_data)
    #             person.teams.add(team)
    #         except Exception as e:
    #             raise serializers.ValidationError(f"Error adding team: {str(e)}")
