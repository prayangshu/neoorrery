from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('body/<int:pk>/<str:body_type>/', views.body_detail, name='body_detail'),
    path('export/', views.export_bodies_csv, name='export_bodies_csv'),
    path('3d-view/', views.three_d_view, name='three_d_view'),
    path('api/orbital-data/', views.fetch_orbital_data, name='fetch_orbital_data'),
    path('login/', auth_views.LoginView.as_view(template_name='orrery/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='orrery/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('toggle-alert/', views.toggle_alert_subscription, name='toggle_alert_subscription'),
    path('update-nasa-data/', views.update_nasa_data, name='update_nasa_data'),
    path('get-close-approaches-now/', views.get_close_approaches_now, name='get_close_approaches_now'),
    path('nasa-data-logs/', views.nasa_data_logs, name='nasa_data_logs'),  # Added log view path
]
