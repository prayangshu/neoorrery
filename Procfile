web: cd NeoOrreryProject && python manage.py collectstatic --noinput && gunicorn NeoOrreryProject.wsgi
worker: celery -A NeoOrreryProject worker -B -l info
