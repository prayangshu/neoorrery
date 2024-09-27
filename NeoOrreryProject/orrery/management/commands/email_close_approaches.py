import smtplib
import ssl
from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from orrery.models import UserProfile
from orrery.utils.nasa_data import fetch_close_approaches
from datetime import datetime


class Command(BaseCommand):
    help = 'Sends email alerts for close approaches of celestial bodies.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for close approaches and sending email alerts...')
        threshold_distance = 100000  # 100,000 km
        close_notify_distance = 10000  # 10,000 km

        # Get users who opted in
        opted_in_users = UserProfile.objects.filter(is_opted_in=True).select_related('user')

        if not opted_in_users.exists():
            self.stdout.write(self.style.WARNING('No users opted-in for close approach alerts.'))
            return

        email_list = [profile.user.email for profile in opted_in_users]

        try:
            close_approaches, critical_approaches = fetch_close_approaches()

            if close_approaches:
                subject = f"NeoOrrery Close Approaches Alert {datetime.now().strftime('%d %B %Y')}"
                message = "The following celestial bodies are approaching Earth within a close range:\n\n"
                critical_approach = False

                for body in close_approaches:
                    message += f"- {body['name']}: {body['distance']} km from Earth\n"
                    if body['is_critical']:
                        critical_approach = True

                if critical_approach:
                    message += "\n⚠️ **Critical Alert**: Some celestial bodies are within 10,000 km of Earth. Immediate attention required!\n"
            else:
                subject = f"No Close Approaches Detected on {datetime.now().strftime('%d %B %Y')}"
                message = "No celestial bodies are approaching Earth within the critical range of 100,000 km.\n"

            # Send email with SSL certificate verification disabled
            self.send_email_with_ssl_override(subject, message, email_list)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully fetched {len(close_approaches)} close approaches. '
                f'{len(critical_approaches)} critical approaches recorded and sent to {len(email_list)} users.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))

    def send_email_with_ssl_override(self, subject, message, email_list):
        """Send an email bypassing SSL verification."""
        try:
            context = ssl._create_unverified_context()

            # Create a message object
            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, email_list)
            msg.content_subtype = 'plain'  # Set content as plain text

            # Connect to the SMTP server with SSL
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(msg.from_email, msg.to, msg.message().as_string())

        except Exception as e:
            raise Exception(f"Error sending email: {e}")
