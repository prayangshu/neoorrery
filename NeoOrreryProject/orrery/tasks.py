# orrery/tasks.py

from celery import shared_task
from .management.commands.fetch_real_time_close_approaches import Command as FetchRealTimeCloseApproachesCommand
from .models import NasaDataLog

@shared_task
def update_real_time_close_approaches(user_id=None):
    """Fetch real-time close approaches and log the action."""
    fetch_real_time_approaches = FetchRealTimeCloseApproachesCommand()
    fetch_real_time_approaches.handle()

    user = None
    if user_id:
        user = User.objects.get(id=user_id)

    NasaDataLog.objects.create(user=user, action='Updated Real-Time Close Approaches')
