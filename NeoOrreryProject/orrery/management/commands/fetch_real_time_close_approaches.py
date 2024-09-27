from django.core.management.base import BaseCommand
from orrery.models import RealTimeCloseApproach
from orrery.utils.nasa_data import fetch_close_approaches

class Command(BaseCommand):
    help = 'Fetches real-time close approaches from NASA and updates the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching real-time close approaches from NASA...')

        threshold_distance = 100000  # 100,000 km
        close_notify_distance = 10000  # 10,000 km

        try:
            # Fetch close approaches data from NASA using the utility function
            close_approaches_data, _ = fetch_close_approaches()

            # Clear existing real-time close approaches
            RealTimeCloseApproach.objects.all().delete()

            # Process the fetched close approaches
            close_approaches = []
            critical_approaches = []

            for body in close_approaches_data:
                distance = body['distance']
                is_critical = distance <= close_notify_distance

                # Categorize into close and critical approaches based on the threshold
                if distance <= threshold_distance:
                    close_approaches.append(body)

                if is_critical:
                    critical_approaches.append(body)

                # Add the close approach to the database
                RealTimeCloseApproach.objects.create(
                    name=body['name'],
                    distance=body['distance'],
                    velocity=body['velocity'],
                    approach_date=body['approach_date'],
                    is_critical=is_critical
                )

            # Log success messages
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(close_approaches)} close approaches.'))
            self.stdout.write(self.style.SUCCESS(f'{len(critical_approaches)} critical approaches recorded.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching real-time close approaches: {e}'))
