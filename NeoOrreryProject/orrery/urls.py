from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('body/<int:pk>/<str:body_type>/', views.body_detail, name='body_detail'),
    path('export/', views.export_bodies_csv, name='export_bodies_csv'),
    path('3d-view/', views.three_d_view, name='three_d_view'),
    path('api/orbital-data/', views.fetch_orbital_data, name='fetch_orbital_data'),
]