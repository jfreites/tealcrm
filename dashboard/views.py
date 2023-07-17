from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from client.models import Client
from lead.models import Lead
from team.models import Team


@login_required
def index(request):
    team = Team.objects.filter(created_by=request.user)[0]

    clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]
    leads = Lead.objects.filter(team=team, converted_to_client=False).order_by('-created_at')[0:5]

    return render(request, 'dashboard/index.html', {
        'clients': clients,
        'leads': leads,
    })
