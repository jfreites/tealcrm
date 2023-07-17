from django import forms

from .models import Team


class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
