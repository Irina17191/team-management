from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Person(models.Model):
    """
    Represents a person who can belong to multiple teams.

    The ManyToManyField is used to allow a person to belong to multiple teams,
    reflecting real-world scenarios where an individual, such as a manager,
    can participate in both the administration and development teams.
    """

    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    teams = models.ManyToManyField(Team, blank=True, related_name="persons")

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["name"]
