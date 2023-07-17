from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EditTeamForm
from .models import Team


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)

    return render(request, 'team/team_detail.html', {
        'team': team,
    })


@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    form = EditTeamForm(instance=team)

    if request.method == 'POST':
        form = EditTeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()

            messages.success(request, 'Team was updated!')

            return redirect('myaccount')

    return render(request, 'team/edit_team.html', {
        'form': form,
        'team': team,
    })
