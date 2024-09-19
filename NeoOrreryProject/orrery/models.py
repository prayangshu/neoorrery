from django.db import models
import requests

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

    @property
    def image_url(self):
        return self.fetch_image_url()

    def fetch_image_url(self):
        api_url = f'https://images-api.nasa.gov/search?q={self.nasa_id}&media_type=image'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('collection', {}).get('items', [])
            if items:
                return items[0].get('links', [])[0].get('href', '')
        return ''

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
