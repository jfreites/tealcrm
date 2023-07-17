from django.urls import path

from . import views

app_name = 'lead'

urlpatterns = [
    path('', views.leads_listing, name='list'),
    path('<pk>/show/', views.lead_detail, name='detail'),
    path('<pk>/edit/', views.edit_lead, name='edit'),
    path('<pk>/delete/', views.delete_lead, name='delete'),
    path('<pk>/convert/', views.convert_to_client, name='convert_to_client'),
    path('add-lead/', views.add_lead, name='add'),
]