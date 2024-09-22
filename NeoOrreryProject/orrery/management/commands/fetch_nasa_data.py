import csv
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from orrery.models import Planet, Comet, Asteroid, CelestialBodyStats


class Command(BaseCommand):
    help = 'Fetches planetary, comet, and NEO (asteroid/PHA) data from NASA APIs and stores it in the database, also creates a CSV file for download.'

    def handle(self, *args, **kwargs):
        api_key = 'WabOZ3Suz7jQnDroucIZHduxXz0EuAWO96H2vt0e'
        neo_url = "https://api.nasa.gov/neo/rest/v1/feed"
        comet_url = "https://data.nasa.gov/resource/b67r-rgxc.json"

        # Get previous stats for calculating percentage changes
        previous_stats = CelestialBodyStats.objects.order_by('-timestamp').first()

        # Add static planetary data first
        self.add_planets()

        # Fetch Near-Earth Comets (NECs)
        self.fetch_comets(comet_url)

        # Date range for NEO data (past to present)
        start_date = datetime(1995, 1, 1)
        end_date = datetime.now()

        # Fetch NEO data in 7-day increments
        self.fetch_neos(api_key, neo_url, start_date, end_date)

        # Calculate the new totals
        total_planets = Planet.objects.count()
        total_comets = Comet.objects.count()
        total_asteroids = Asteroid.objects.count()
        total_pha = Asteroid.objects.filter(is_potentially_hazardous=True).count()
        total_bodies = total_planets + total_comets + total_asteroids

        # Create new stats entry
        stats = CelestialBodyStats(
            total_bodies=total_bodies,
            total_planets=total_planets,
            total_comets=total_comets,
            total_asteroids=total_asteroids,
            total_pha=total_pha
        )
        stats.save_stats(previous_stats)

        # Create the CSV file after fetching the data
        self.create_csv()

        self.stdout.write(self.style.SUCCESS(f'Data fetched and updated successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total Celestial Bodies: {total_bodies}'))
        self.stdout.write(self.style.SUCCESS(f'Planets: {total_planets} ({stats.planet_change}%)'))
        self.stdout.write(self.style.SUCCESS(f'Comets: {total_comets} ({stats.comet_change}%)'))
        self.stdout.write(self.style.SUCCESS(f'Asteroids: {total_asteroids} ({stats.asteroid_change}%)'))
        self.stdout.write(self.style.SUCCESS(f'PHA: {total_pha} ({stats.pha_change}%)'))

    def add_planets(self):
        planets = [
            {'name': 'Mercury', 'size': 4879, 'distance': 57910000, 'nasa_id': 'mercury',
             'semi_major_axis': 0.387, 'eccentricity': 0.2056, 'inclination': 7.005,
             'argument_of_periapsis': 29.124, 'longitude_of_ascending_node': 48.331, 'mean_anomaly': 174.796},
            {'name': 'Venus', 'size': 12104, 'distance': 108200000, 'nasa_id': 'venus',
             'semi_major_axis': 0.723, 'eccentricity': 0.0067, 'inclination': 3.3946,
             'argument_of_periapsis': 54.852, 'longitude_of_ascending_node': 76.680, 'mean_anomaly': 50.115},
            # Add other planets...
        ]

        for planet in planets:
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
                semi_major_axis = comet.get('a', None)
                eccentricity = comet.get('e', None)
                inclination = comet.get('i_deg', None)
                perihelion_distance = comet.get('q_au_1', None)
                period = comet.get('p_yr', None)

                distance = None
                if perihelion_distance:
                    try:
                        distance = float(perihelion_distance) * 149597870.7
                    except (TypeError, ValueError):
                        self.stdout.write(self.style.ERROR(f"Invalid perihelion distance for comet {name}"))

                try:
                    obj, created = Comet.objects.update_or_create(
                        nasa_id=comet.get('object', 'TBD'),
                        defaults={
                            'name': name,
                            'eccentricity': eccentricity,
                            'inclination': inclination,
                            'distance': distance,
                            'orbital_period': period,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Added new Comet: {obj.name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated Comet: {obj.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error saving comet: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch comet data: {response.status_code}'))

    def fetch_neos(self, api_key, url, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)
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

                        try:
                            obj, created = Asteroid.objects.update_or_create(
                                nasa_id=nasa_id,
                                defaults={
                                    'name': name,
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
                self.stdout.write(self.style.ERROR(f'Failed to fetch NEO data: {response.status_code}'))

            current_date = next_date

    def calculate_percentage_change(self, initial, current):
        if initial == 0:
            return "N/A"  # No data previously
        return round(((current - initial) / initial) * 100, 2)

    def create_csv(self):
        """Creates a CSV file with celestial bodies data."""
        file_path = 'celestial_bodies_data.csv'
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Body Type', 'Size (meters)', 'Distance from Earth (km)', 'Last Updated'])

            # Fetch all celestial bodies
            planets = Planet.objects.all()
            comets = Comet.objects.all()
            asteroids = Asteroid.objects.all()

            # Write planet data to CSV
            for planet in planets:
                writer.writerow([planet.name, 'Planet', planet.size, planet.distance, planet.last_updated])

            # Write comet data to CSV
            for comet in comets:
                writer.writerow([comet.name, 'Comet', comet.size, comet.distance, comet.last_updated])

            # Write asteroid data to CSV (PHA and non-PHA)
            for asteroid in asteroids:
                body_type = 'PHA' if asteroid.is_potentially_hazardous else 'Asteroid'
                writer.writerow([asteroid.name, body_type, asteroid.size, asteroid.distance, asteroid.last_updated])

        self.stdout.write(self.style.SUCCESS(f'CSV file created: {file_path}'))
