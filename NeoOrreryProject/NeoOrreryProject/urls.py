from django.contrib import admin
from django.urls import path, include  # Ensure path and include are imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 'path' should now be correctly recognized
    path('', include('orrery.urls')),  # Ensure your app's URLs are included here
]

# This will serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
