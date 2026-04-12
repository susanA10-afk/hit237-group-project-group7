from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.urls import reverse_lazy
from .models import (
    YoungPerson, Offence, Intervention,
    CaseWorker, CourtHearing
)


class YoungPersonListView(LoginRequiredMixin, ListView):
    model = YoungPerson
    template_name = 'justice/youngperson_list.html'
    context_object_name = 'youngpeople'

    def get_queryset(self):
        return YoungPerson.objects.select_related().prefetch_related(
            'caseworkers', 'offences', 'interventions'
        )


class YoungPersonDetailView(LoginRequiredMixin, DetailView):
    model = YoungPerson
    template_name = 'justice/youngperson_detail.html'
    context_object_name = 'youngperson'

    def get_queryset(self):
        return YoungPerson.objects.prefetch_related(
            'offences', 'interventions', 'hearings'
        )


class YoungPersonCreateView(LoginRequiredMixin, CreateView):
    model = YoungPerson
    template_name = 'justice/youngperson_form.html'
    fields = [
        'first_name', 'last_name', 'date_of_birth',
        'gender', 'postcode', 'risk_level'
    ]
    success_url = reverse_lazy('justice:youngperson-list')


class OffenceCreateView(LoginRequiredMixin, CreateView):
    model = Offence
    template_name = 'justice/offence_form.html'
    fields = [
        'young_person', 'offence_type', 'date_of_offence',
        'location', 'severity', 'description'
    ]
    success_url = reverse_lazy('justice:youngperson-list')


class InterventionCreateView(LoginRequiredMixin, CreateView):
    model = Intervention
    template_name = 'justice/intervention_form.html'
    fields = [
        'young_person', 'assigned_worker', 'intervention_type',
        'start_date', 'end_date', 'status', 'outcome'
    ]
    success_url = reverse_lazy('justice:youngperson-list')


class InterventionUpdateView(LoginRequiredMixin, UpdateView):
    model = Intervention
    template_name = 'justice/intervention_form.html'
    fields = ['status', 'end_date', 'outcome']
    success_url = reverse_lazy('justice:youngperson-list')


class CaseWorkerDashboardView(LoginRequiredMixin, ListView):
    model = YoungPerson
    template_name = 'justice/dashboard.html'
    context_object_name = 'youngpeople'

    def get_queryset(self):
        return YoungPerson.objects.prefetch_related(
            'caseworkers', 'offences'
        ).filter(risk_level='high')