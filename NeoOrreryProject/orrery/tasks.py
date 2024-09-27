# orrery/tasks.py

from celery import shared_task
from .management.commands.fetch_nasa_data import Command as FetchNASADataCommand

@shared_task
def fetch_nasa_data_task():
    """Fetch NASA data using the fetch_nasa_data management command."""
    fetch_nasa_data = FetchNASADataCommand()
    fetch_nasa_data.handle()
