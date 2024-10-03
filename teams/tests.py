from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from teams.models import Team, Person


class PersonAPITests(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Development")
        self.person_data = {
            "name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "teams": [self.team.id],
        }
        self.person_url = reverse("teams:person-list")

    def test_create_person(self):
        response = self.client.post(self.person_url, self.person_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get().name, "John")

    def test_list_persons(self):
        person = Person.objects.create(
            name="John", last_name="Doe", email="john.doe@example.com"
        )
        person.teams.add(self.team)
        response = self.client.get(self.person_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_person(self):
        person = Person.objects.create(
            name="John", last_name="Doe", email="john.doe@example.com"
        )
        person.teams.add(self.team)

        update_data = {
            "name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "teams": [self.team.id],
        }

        response = self.client.patch(
            reverse("teams:person-detail", args=[person.id]), update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person.refresh_from_db()
        self.assertEqual(person.name, "Jane")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.email, "jane.doe@example.com")

    def test_delete_person(self):
        person = Person.objects.create(
            name="John", last_name="Doe", email="john.doe@example.com"
        )
        person.teams.add(self.team)
        response = self.client.delete(reverse("teams:person-detail", args=[person.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)


class TeamAPITests(APITestCase):
    def setUp(self):
        self.team_data = {"name": "Development"}
        self.team_url = reverse("teams:team-list")

    def test_create_team(self):
        response = self.client.post(self.team_url, self.team_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, "Development")

    def test_list_teams(self):
        Team.objects.create(name="Development")
        Team.objects.create(name="Design")

        response = self.client.get(self.team_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_team(self):
        team = Team.objects.create(name="Development")
        update_data = {"name": "Updated Development"}

        response = self.client.patch(
            reverse("teams:team-detail", args=[team.id]), update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team.refresh_from_db()
        self.assertEqual(team.name, "Updated Development")

    def test_delete_team(self):
        team = Team.objects.create(name="Development")
        response = self.client.delete(reverse("teams:team-detail", args=[team.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)
