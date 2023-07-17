from django.urls import path

from . import views

app_name = 'lead'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('<int:pk>', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    path('<pk>/convert/', views.ConvertToClientView.as_view(), name='convert_to_client'),
    path('add-lead/', views.LeadCreateView.as_view(), name='add'),
]