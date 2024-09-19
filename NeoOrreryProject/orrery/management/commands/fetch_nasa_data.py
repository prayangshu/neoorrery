import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from orrery.models import Planet, Comet, Asteroid


class Command(BaseCommand):
    help = 'Fetches planetary, comet, and NEO (asteroid/PHA) data from NASA APIs and stores it in the database.'

    def handle(self, *args, **kwargs):
        api_key = 'WabOZ3Suz7jQnDroucIZHduxXz0EuAWO96H2vt0e'
        neo_url = "https://api.nasa.gov/neo/rest/v1/feed"
        comet_url = "https://data.nasa.gov/resource/b67r-rgxc.json"  # Comet API URL

        # Add static planetary data first
        self.add_planets()

        # Fetch Near-Earth Comets (NECs)
        self.fetch_comets(comet_url)

        # Date range for NEO data (past to present)
        start_date = datetime(1995, 1, 1)  # Start fetching from January 1, 1995
        end_date = datetime.now()  # Up to the current date

        # Fetch NEO data in 7-day increments
        self.fetch_neos(api_key, neo_url, start_date, end_date)

        self.stdout.write(self.style.SUCCESS('Data fetched and updated successfully!'))

    def add_planets(self):
        planets = [
            {
                'name': 'Mercury', 'size': 4879, 'distance': 57910000, 'nasa_id': 'mercury',
                'semi_major_axis': 0.387, 'eccentricity': 0.2056, 'inclination': 7.005,
                'argument_of_periapsis': 29.124, 'longitude_of_ascending_node': 48.331,
                'mean_anomaly': 174.796
            },
            {
                'name': 'Venus', 'size': 12104, 'distance': 108200000, 'nasa_id': 'venus',
                'semi_major_axis': 0.723, 'eccentricity': 0.0067, 'inclination': 3.3946,
                'argument_of_periapsis': 54.852, 'longitude_of_ascending_node': 76.680,
                'mean_anomaly': 50.115
            },
            {
                'name': 'Earth', 'size': 12742, 'distance': 149600000, 'nasa_id': 'earth',
                'semi_major_axis': 1.000, 'eccentricity': 0.0167, 'inclination': 0.00005,
                'argument_of_periapsis': 114.20783, 'longitude_of_ascending_node': -11.26064,
                'mean_anomaly': 357.51716
            },
            {
                'name': 'Mars', 'size': 6779, 'distance': 227900000, 'nasa_id': 'mars',
                'semi_major_axis': 1.524, 'eccentricity': 0.0934, 'inclination': 1.850,
                'argument_of_periapsis': 286.502, 'longitude_of_ascending_node': 49.558,
                'mean_anomaly': 19.373
            },
            {
                'name': 'Jupiter', 'size': 139820, 'distance': 778500000, 'nasa_id': 'jupiter',
                'semi_major_axis': 5.203, 'eccentricity': 0.0489, 'inclination': 1.304,
                'argument_of_periapsis': 273.867, 'longitude_of_ascending_node': 100.464,
                'mean_anomaly': 19.650
            },
            {
                'name': 'Saturn', 'size': 116460, 'distance': 1434000000, 'nasa_id': 'saturn',
                'semi_major_axis': 9.537, 'eccentricity': 0.0565, 'inclination': 2.485,
                'argument_of_periapsis': 339.392, 'longitude_of_ascending_node': 113.665,
                'mean_anomaly': 317.020
            },
            {
                'name': 'Uranus', 'size': 50724, 'distance': 2871000000, 'nasa_id': 'uranus',
                'semi_major_axis': 19.191, 'eccentricity': 0.0463, 'inclination': 0.772,
                'argument_of_periapsis': 96.998, 'longitude_of_ascending_node': 74.006,
                'mean_anomaly': 142.238
            },
            {
                'name': 'Neptune', 'size': 49244, 'distance': 4495000000, 'nasa_id': 'neptune',
                'semi_major_axis': 30.069, 'eccentricity': 0.0086, 'inclination': 1.769,
                'argument_of_periapsis': 273.187, 'longitude_of_ascending_node': 131.784,
                'mean_anomaly': 256.228
            }
        ]

        for planet in planets:
            description = f"{planet['name']} is a planet with a diameter of {planet['size']} kilometers and a distance of {planet['distance']} kilometers from the Sun."
            try:
                obj, created = Planet.objects.update_or_create(
                    nasa_id=planet['nasa_id'],
                    defaults={
                        'name': planet['name'],
                        'size': planet['size'],
                        'distance': planet['distance'],
                        'semi_major_axis': planet['semi_major_axis'],
                        'eccentricity': planet['eccentricity'],
                        'inclination': planet['inclination'],
                        'argument_of_periapsis': planet['argument_of_periapsis'],
                        'longitude_of_ascending_node': planet['longitude_of_ascending_node'],
                        'mean_anomaly': planet['mean_anomaly'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added new Planet: {obj.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated Planet: {obj.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving planet: {e}'))

    def fetch_comets(self, url):
        limit = 170
        params = {'$limit': limit}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            comets = response.json()

            for comet in comets:
                name = comet.get('object_name', 'Unknown Comet')
                semi_major_axis = comet.get('a', None)  # Keplerian semi-major axis
                eccentricity = comet.get('e', None)  # Keplerian eccentricity
                inclination = comet.get('i_deg', None)  # Orbital inclination
                perihelion_distance = comet.get('q_au_1', None)  # Closest distance to the Sun in AU
                period = comet.get('p_yr', None)  # Orbital period in years

                # Handle comet distance and size estimation
                distance = None
                if perihelion_distance:
                    try:
                        distance = float(perihelion_distance) * 149597870.7  # Convert AU to kilometers
                    except (TypeError, ValueError):
                        self.stdout.write(self.style.ERROR(f"Invalid perihelion distance for comet {name}"))

                nasa_id = comet.get('object', 'TBD')
                description = f"{name} is a comet with an eccentricity of {eccentricity} and a perihelion distance of {perihelion_distance} AU."

                try:
                    obj, created = Comet.objects.update_or_create(
                        nasa_id=nasa_id,
                        defaults={
                            'name': name,
                            'eccentricity': eccentricity,
                            'inclination': inclination,
                            'distance': distance,
                            'description': description,
                            'orbital_period': period
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Added new Comet: {obj.name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated Comet: {obj.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error saving comet: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch comet data: {response.status_code} - {response.text}'))

    def fetch_neos(self, api_key, url, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)  # Move 7 days ahead

            params = {
                "api_key": api_key,
                "start_date": current_date.strftime('%Y-%m-%d'),
                "end_date": next_date.strftime('%Y-%m-%d')
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                for neo_date in data['near_earth_objects']:
                    for item in data['near_earth_objects'][neo_date]:
                        is_hazardous = item.get('is_potentially_hazardous_asteroid', False)
                        body_type = 'PHA' if is_hazardous else 'Asteroid'
                        name = item.get('name', 'Unknown')
                        size = item.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_max', 0)
                        distance = float(item.get('close_approach_data', [])[0].get('miss_distance', {}).get('kilometers', 0))
                        nasa_id = item['id']

                        description = f"{name} is a {body_type.lower()} with an estimated diameter of {size} meters. It is currently {distance} kilometers away from Earth."

                        try:
                            obj, created = Asteroid.objects.update_or_create(
                                nasa_id=nasa_id,
                                defaults={
                                    'name': name,
                                    'description': description,
                                    'size': size,
                                    'distance': distance,
                                    'is_potentially_hazardous': is_hazardous,
                                }
                            )
                            if created:
                                self.stdout.write(self.style.SUCCESS(f'Added new {body_type}: {obj.name}'))
                            else:
                                self.stdout.write(self.style.SUCCESS(f'Updated {body_type}: {obj.name}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error saving {body_type}: {e}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch NEO data: {response.status_code} - {response.text}'))

            current_date = next_date
