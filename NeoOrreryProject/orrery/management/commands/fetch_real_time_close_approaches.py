from django.core.management.base import BaseCommand
from orrery.models import RealTimeCloseApproach, UserProfile
from orrery.utils.nasa_data import fetch_close_approaches


class Command(BaseCommand):
    help = 'Fetches real-time close approaches from NASA and updates the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching real-time close approaches from NASA...')

        try:
            # Fetch close approaches data from NASA
            close_approaches_data, _ = fetch_close_approaches()

            # Clear existing real-time close approaches from the database
            RealTimeCloseApproach.objects.all().delete()

            close_approaches = []
            critical_approaches = []

            # Fetch all user profiles to process personalized distances
            user_profiles = UserProfile.objects.all()

            for body in close_approaches_data:
                distance = body['distance']
                is_critical = False

                # Check if the distance falls within any user's threshold
                for profile in user_profiles:
                    if distance <= profile.real_time_distance:
                        close_approaches.append(body)
                    if distance <= profile.critical_distance:
                        critical_approaches.append(body)
                        is_critical = True

                # Store the close approach in the database
                RealTimeCloseApproach.objects.create(
                    name=body['name'],
                    distance=distance,
                    velocity=body['velocity'],
                    approach_date=body['approach_date'],
                    is_critical=is_critical
                )

            # Log success messages
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(close_approaches)} close approaches.'))
            self.stdout.write(self.style.SUCCESS(f'{len(critical_approaches)} critical approaches recorded.'))

        except Exception as e:
            # Handle and log any errors
            self.stdout.write(self.style.ERROR(f'Error fetching real-time close approaches: {e}'))
