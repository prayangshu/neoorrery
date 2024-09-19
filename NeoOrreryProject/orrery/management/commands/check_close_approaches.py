
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from orrery.models import CelestialBody

class Command(BaseCommand):
    help = 'Checks for close approaches of celestial bodies and sends alerts'

    def handle(self, *args, **kwargs):
        # Define a threshold for a "close approach" (e.g., 100,000 km)
        threshold_distance = 100000  # 100,000 kilometers

        # Get celestial bodies that are within this distance from Earth
        close_approaches = CelestialBody.objects.filter(distance__lt=threshold_distance)

        if close_approaches.exists():
            subject = "Alert: Close Approach of Celestial Bodies"
            message = "The following celestial bodies are approaching Earth within a close range:\n\n"
            for body in close_approaches:
                message += f"{body.name} - {body.distance} km\n"

            try:
                send_mail(
                    subject,
                    message,
                    'mail@prayangshu.com',  # Sender email
                    ['prayangshu634479@gmail.com'],  # Recipient email
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('Close approach alerts sent successfully!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('No close approaches detected.'))
