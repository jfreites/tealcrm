from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Userprofile
from team.models import Team, Plan


def signup(request):
    # jfreites / xjypAdjT2xFn
    # bamba / 52rSk2g5dbhR
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            Userprofile.objects.create(user=user)

            plan = Plan.objects.first()

            # TODO: implement the ability to register with an invitation from a current team
            team = Team.objects.create(name='Demo Team', plan=plan, created_by=user)
            team.members.add(user)
            team.save()

            return redirect('login')

    return render(request, 'userprofile/signup.html', {'form': form})


@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user)[0]

    return render(request, 'userprofile/myaccount.html', {'team': team})
