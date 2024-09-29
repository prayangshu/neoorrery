web: cd NeoOrreryProject && python manage.py collectstatic --noinput && gunicorn NeoOrreryProject.wsgi
worker: celery -A NeoOrreryProject worker -l info
beat: celery -A NeoOrreryProject beat -l info
