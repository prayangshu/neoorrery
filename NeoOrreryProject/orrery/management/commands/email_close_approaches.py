from django.core.management.base import BaseCommand
from orrery.models import UserProfile
from orrery.utils.nasa_data import fetch_close_approaches
from django.core.mail import send_mail
from datetime import datetime
import smtplib
import ssl  # Import the ssl module


class Command(BaseCommand):
    help = 'Sends email alerts for close approaches of celestial bodies.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for close approaches and sending email alerts...')

        # Fetch users who have opted into alerts
        opted_in_users = UserProfile.objects.filter(is_opted_in=True).select_related('user')

        if not opted_in_users.exists():
            self.stdout.write(self.style.WARNING('No users opted in for close approach alerts.'))
            return

        try:
            # Fetch close approaches data
            close_approaches_data, _ = fetch_close_approaches()

            # Loop through each user and send personalized email
            for profile in opted_in_users:
                user_email = profile.user.email
                user_real_time_distance = profile.real_time_distance
                user_critical_distance = profile.critical_distance

                user_close_approaches = []
                critical_alert = False

                # Check which close approaches match the user's set distance preferences
                for body in close_approaches_data:
                    distance = body['distance']
                    if distance <= user_real_time_distance:
                        user_close_approaches.append(body)
                    if distance <= user_critical_distance:
                        critical_alert = True

                # Prepare email content
                subject = f"NeoOrrery Close Approaches Alert - {datetime.now().strftime('%d %B %Y')}"
                if user_close_approaches:
                    message = "The following celestial bodies are approaching Earth within your set ranges:\n\n"
                    for body in user_close_approaches:
                        message += f"- {body['name']}: {body['distance']} km from Earth\n"
                    if critical_alert:
                        message += "\n⚠️ **Critical Alert**: Some celestial bodies are within your critical range. Immediate attention required!\n"
                else:
                    message = "No celestial bodies are currently approaching Earth within your set ranges."

                # Send the email to the user
                try:
                    # Create a secure SSL context
                    context = ssl.create_default_context()
                    context.check_hostname = False  # Ignore hostname check
                    context.verify_mode = ssl.CERT_NONE  # Disable SSL certificate verification

                    with smtplib.SMTP_SSL('smtp.hostinger.com', 465, context=context) as server:
                        server.login('no-reply@neoorrery.space', 'NASASPACE2024@neo')  # Login
                        server.sendmail('no-reply@neoorrery.space', user_email, f"Subject: {subject}\n\n{message}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error sending email to {user_email}: {e}"))

            self.stdout.write(self.style.SUCCESS('Email alerts sent successfully.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
