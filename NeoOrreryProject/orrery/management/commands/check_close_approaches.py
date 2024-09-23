from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from orrery.models import Planet, Comet, Asteroid, UserProfile
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Command(BaseCommand):
    help = 'Checks for close approaches of celestial bodies and sends alerts to opted-in users.'

    def handle(self, *args, **kwargs):
        threshold_distance = 100000  # 100,000 km
        close_notify_distance = 10000  # 10,000 km

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
            if settings.DEBUG:
                self.send_email_with_ssl_override(subject, message, email_list)
            else:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    email_list,
                    fail_silently=False,
                )

            self.stdout.write(self.style.SUCCESS(f'Close approach alerts sent successfully to {len(email_list)} users.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))

    def send_email_with_ssl_override(self, subject, message, email_list):
        msg = MIMEMultipart()
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = ', '.join(email_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Connect to the SMTP server
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.DEFAULT_FROM_EMAIL, email_list, msg.as_string())

        except Exception as e:
            raise e
