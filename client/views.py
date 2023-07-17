from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EditClientForm
from .models import Client

from team.models import Team


@login_required
def clients_listing(request):
    clients = Client.objects.filter(created_by=request.user, deleted_at=None)

    return render(request, 'client/clients_listing.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    return render(request, 'client/client_detail.html', {'client': client})


@login_required
def add_client(request):
    form = EditClientForm()

    if request.method == 'POST':
        form = EditClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter()

            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            

            messages.success(request, 'The client was updated')

            return redirect('clients_listing')

    return render(request, 'client/edit_lead.html', {'form': form})


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    form = EditClientForm(instance=client)

    if request.method == 'POST':
        form = EditClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'The client was updated')

            return redirect('clients_listing')

    return render(request, 'client/edit_lead.html', {'form': form})


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.soft_delete()

    messages.success(request, 'The client was deleted')

    return redirect('clients_listing')
