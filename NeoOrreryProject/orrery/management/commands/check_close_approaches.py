from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from orrery.models import Planet, Comet, Asteroid

class Command(BaseCommand):
    help = 'Checks for close approaches of celestial bodies and sends alerts'

    def handle(self, *args, **kwargs):
        threshold_distance = 100000
        close_approaches_planets = Planet.objects.filter(distance__lt=threshold_distance)
        close_approaches_comets = Comet.objects.filter(distance__lt=threshold_distance)
        close_approaches_asteroids = Asteroid.objects.filter(distance__lt=threshold_distance)
        close_approaches = list(close_approaches_planets) + list(close_approaches_comets) + list(close_approaches_asteroids)

        if close_approaches:
            subject = "Alert: Close Approach of Celestial Bodies"
            message = "The following celestial bodies are approaching Earth within a close range:\n\n"
            for body in close_approaches:
                message += f"{body.name} - {body.distance} km\n"

            try:
                send_mail(
                    subject,
                    message,
                    'mail@prayangshu.com',
                    ['prayangshu634479@gmail.com'],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('Close approach alerts sent successfully!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('No close approaches detected.'))
