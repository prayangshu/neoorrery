from django.db import models
from django.utils import timezone


class CelestialBody(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    nasa_id = models.CharField(max_length=100, unique=True, default="TBD")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"

    def get_body_type(self):
        """Return the type of celestial body (to be overridden by subclasses)."""
        return "CelestialBody"


class Planet(CelestialBody):
    semi_major_axis = models.FloatField(blank=True, null=True)
    eccentricity = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)
    argument_of_periapsis = models.FloatField(blank=True, null=True)
    longitude_of_ascending_node = models.FloatField(blank=True, null=True)
    mean_anomaly = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Planet: {self.name}"

    def get_body_type(self):
        return "Planet"


class Comet(CelestialBody):
    orbital_period = models.FloatField(blank=True, null=True)
    eccentricity = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)
    argument_of_periapsis = models.FloatField(blank=True, null=True)
    longitude_of_ascending_node = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Comet: {self.name}"

    def get_body_type(self):
        return "Comet"


class Asteroid(CelestialBody):
    is_potentially_hazardous = models.BooleanField(default=False)

    def __str__(self):
        if self.is_potentially_hazardous:
            return f"Potentially Hazardous Asteroid: {self.name}"
        else:
            return f"Asteroid: {self.name}"

    def get_body_type(self):
        if self.is_potentially_hazardous:
            return "PHA"
        else:
            return "Asteroid"


class CelestialBodyStats(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    total_bodies = models.IntegerField(default=0)
    total_planets = models.IntegerField(default=0)
    total_comets = models.IntegerField(default=0)
    total_asteroids = models.IntegerField(default=0)
    total_pha = models.IntegerField(default=0)
    planet_change = models.FloatField(blank=True, null=True)
    comet_change = models.FloatField(blank=True, null=True)
    asteroid_change = models.FloatField(blank=True, null=True)
    pha_change = models.FloatField(blank=True, null=True)

    def save_stats(self, previous_stats=None):

        if previous_stats:
            self.planet_change = self.calculate_change(previous_stats.total_planets, self.total_planets)
            self.comet_change = self.calculate_change(previous_stats.total_comets, self.total_comets)
            self.asteroid_change = self.calculate_change(previous_stats.total_asteroids, self.total_asteroids)
            self.pha_change = self.calculate_change(previous_stats.total_pha, self.total_pha)
        self.save()

    @staticmethod
    def calculate_change(old_value, new_value):
        if old_value == 0:
            return None  # Return None if there was no previous data
        return round(((new_value - old_value) / old_value) * 100, 2)

    def __str__(self):
        return f"Celestial Body Stats at {self.timestamp}"
