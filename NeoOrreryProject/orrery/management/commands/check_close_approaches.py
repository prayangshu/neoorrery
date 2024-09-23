from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from orrery.models import Planet, Comet, Asteroid, UserProfile
from datetime import datetime

class Command(BaseCommand):
    help = 'Checks for close approaches of celestial bodies and sends alerts to opted-in users.'

    def handle(self, *args, **kwargs):
        threshold_distance = 100000
        close_notify_distance = 10000

        opted_in_users = UserProfile.objects.filter(is_opted_in=True).select_related('user')

        if not opted_in_users.exists():
            self.stdout.write(self.style.WARNING('No users opted-in for close approach alerts.'))
            return

        email_list = [profile.user.email for profile in opted_in_users]

        close_approaches_planets = Planet.objects.filter(distance__lt=threshold_distance)
        close_approaches_comets = Comet.objects.filter(distance__lt=threshold_distance)
        close_approaches_asteroids = Asteroid.objects.filter(distance__lt=threshold_distance)

        close_approaches = list(close_approaches_planets) + list(close_approaches_comets) + list(close_approaches_asteroids)

        if close_approaches:
            subject = f"NeoOrrery Close Approaches Alert {datetime.now().strftime('%d %B %Y')}"
            message = "The following celestial bodies are approaching Earth within a close range:\n\n"
            critical_approach = False

            for body in close_approaches:
                message += f"- {body.name}: {body.distance} km from Earth\n"
                if body.distance < close_notify_distance:
                    critical_approach = True

            if critical_approach:
                message += "\n⚠️ **Critical Alert**: Some celestial bodies are within 10,000 km of Earth. Immediate attention required!\n"

        else:
            subject = f"No Close Approaches Detected on {datetime.now().strftime('%d %B %Y')}"
            message = "No celestial bodies are approaching Earth within the critical range of 100,000 km.\n"

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Sender email
                email_list,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Close approach alerts sent successfully to {len(email_list)} users.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))
