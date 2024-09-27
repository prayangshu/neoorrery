from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg', null=True, blank=True)
    is_opted_in = models.BooleanField(default=False)  # Tracks whether the user has opted into alerts

    def __str__(self):
        return f"{self.user.username}'s profile"

class CelestialBody(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)  # in kilometers/meters
    distance = models.FloatField(blank=True, null=True)  # in kilometers
    nasa_id = models.CharField(max_length=100, unique=True, default="TBD")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This is an abstract model, not a table

    def __str__(self):
        return self.name

    def get_body_type(self):
        """Return the type of celestial body (to be overridden by subclasses)."""
        return "CelestialBody"

class Planet(CelestialBody):
    semi_major_axis = models.FloatField(blank=True, null=True)  # in AU
    eccentricity = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)  # in degrees
    argument_of_periapsis = models.FloatField(blank=True, null=True)  # in degrees
    longitude_of_ascending_node = models.FloatField(blank=True, null=True)  # in degrees
    mean_anomaly = models.FloatField(blank=True, null=True)  # in degrees

    def __str__(self):
        return f"Planet: {self.name}"

    def get_body_type(self):
        return "Planet"

class Comet(CelestialBody):
    orbital_period = models.FloatField(blank=True, null=True)  # in years
    eccentricity = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)  # in degrees
    argument_of_periapsis = models.FloatField(blank=True, null=True)  # in degrees
    longitude_of_ascending_node = models.FloatField(blank=True, null=True)  # in degrees

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
        return "PHA" if self.is_potentially_hazardous else "Asteroid"

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
        """Calculate changes compared to previous stats and save the new stats."""
        if previous_stats:
            self.planet_change = self.calculate_change(previous_stats.total_planets, self.total_planets)
            self.comet_change = self.calculate_change(previous_stats.total_comets, self.total_comets)
            self.asteroid_change = self.calculate_change(previous_stats.total_asteroids, self.total_asteroids)
            self.pha_change = self.calculate_change(previous_stats.total_pha, self.total_pha)
        self.save()

    @staticmethod
    def calculate_change(old_value, new_value):
        """Calculate the percentage change between old and new values."""
        if old_value == 0:
            return None
        return round(((new_value - old_value) / old_value) * 100, 2)

    def __str__(self):
        return f"Celestial Body Stats at {self.timestamp}"

class NasaDataLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # Log what action was performed (e.g., "Updated NASA Data", "Requested Close Approaches Alert")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"

class RealTimeCloseApproach(models.Model):
    name = models.CharField(max_length=255)
    nasa_id = models.CharField(max_length=255)
    distance = models.FloatField(help_text="Distance from Earth in kilometers")
    velocity = models.FloatField(help_text="Velocity in km/h")
    approach_date = models.DateField()
    is_critical = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.distance} km"
