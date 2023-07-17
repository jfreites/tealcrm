from django.urls import path

from . import views

urlpatterns = [
    path('', views.clients_listing, name='clients_listing'),
    path('<int:pk>/', views.client_detail, name='client_detail'),
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('export/', views.clients_export, name='clients_export'),
]
