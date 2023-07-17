from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import AddCommentForm
from .models import Lead, Comment

from client.models import Client
from team.models import Team


class LeadListView(ListView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)


class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['comments'] = Comment.objects.filter(lead_id=self.kwargs.get('pk'))

        return context


class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('lead:list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'The lead was deleted')
        return super(LeadDeleteView, self).form_valid(form)



class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('lead:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Lead'

        return context


class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('lead:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['form_title'] = 'Add Lead'
        context['total_leads'] = Lead.objects.filter(created_by=self.request.user, converted_to_client=False).count()

        return context

    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        team = Team.objects.filter(created_by=self.request.user)[0]

        form.instance.team = team
        form.instance.created_by = self.request.user

        return super().form_valid(form)


class ConvertToClientView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(args, kwargs, self.args, self.kwargs)
        lead = get_object_or_404(Lead, created_by=request.user, pk=self.kwargs.get('pk'))
        team = Team.objects.filter(created_by=request.user)[0]
        clients_total = Client.objects.filter(team=team).count()

        if clients_total > team.plan.max_clients:
            messages.success(request, 'You have reached the limit of clients.')
            return redirect('lead:list')

        Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=lead.team,
        )

        lead.converted_to_client = True
        lead.save()

        messages.success(request, 'The lead was converted to a client')

        return redirect('lead:list')
    

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        team = Team.objects.filter(created_by=request.user)[0]
        
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

            messages.success(request, 'Your comment was saved.')

        return redirect('lead:detail', pk=pk)
