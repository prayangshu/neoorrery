from django.contrib import admin
from django.urls import path, include  # Ensure path and include are imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),

    # Include URLs from the 'orrery' app
    path('', include('orrery.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
