from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from core.views import index, about
from team.views import edit_team, team_detail
from userprofile.views import signup, myaccount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/my-account/', myaccount, name='myaccount'),
    path('dashboard/teams/<int:pk>/', team_detail, name='team_detail'),
    path('dashboard/teams/<int:pk>/edit/', edit_team, name='edit_team'),
    path('dashboard/', include('dashboard.urls')),
    path('about/', about, name='about'),
    path('sign-up/', signup, name='signup'),
    path('log-in/', LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('log-out/', LogoutView.as_view(), name='logout'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
