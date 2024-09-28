# orrery/tasks.py

from celery import shared_task
from .management.commands.fetch_nasa_data import Command as FetchNASADataCommand
from .management.commands.fetch_real_time_close_approaches import Command as FetchRealTimeCloseApproachesCommand
from .models import NasaDataLog

@shared_task
def fetch_nasa_data_task():
    """Fetch NASA data using the fetch_nasa_data management command."""
    fetch_nasa_data = FetchNASADataCommand()
    fetch_nasa_data.handle()
    # Log the action
    NasaDataLog.objects.create(user=None, action='Fetched NASA data')

@shared_task
def update_real_time_close_approaches():
    """Fetch real-time close approaches using the fetch_real_time_close_approaches management command."""
    fetch_command = FetchRealTimeCloseApproachesCommand()
    fetch_command.handle()
    # Log the action
    NasaDataLog.objects.create(user=None, action='Updated Real-Time Close Approaches')
