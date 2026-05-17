from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    YoungPerson, Offence, Intervention,
    CaseWorker, CourtHearing
)
from .services import (
    get_all_young_persons,
    get_high_risk_cases,
    get_young_person_by_id,
    record_offence,
    assign_intervention,
    get_dashboard_stats
)
from .exceptions import (
    YoungPersonNotFound,
    InterventionLimitExceeded
)

class AdminRequiredMixin(LoginRequiredMixin):
    """Only admin users can access this view."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if hasattr(request.user, 'role') and request.user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('justice:youngperson-list')
        return super().dispatch(request, *args, **kwargs)


class YoungPersonListView(LoginRequiredMixin, ListView):
    model = YoungPerson
    template_name = 'justice/youngperson_list.html'
    context_object_name = 'youngpeople'
    paginate_by = 10
    ordering = ['last_name', 'first_name']  # add this line

    def get_queryset(self):
        queryset = get_all_young_persons().annotate(
            offence_count=Count('offences')
        ).order_by('last_name', 'first_name')  # add this
        if hasattr(self.request.user, 'caseworker'):
            queryset = queryset.filter(
                caseworkers=self.request.user.caseworker
            )
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset

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


class InterventionListView(LoginRequiredMixin, ListView):
    model = Intervention
    template_name = 'justice/intervention_list.html'
    context_object_name = 'interventions'

    def get_queryset(self):
        return Intervention.objects.select_related(
            'young_person', 'assigned_worker'
        )


class CaseWorkerDashboardView(LoginRequiredMixin, ListView):
    model = YoungPerson
    template_name = 'justice/dashboard.html'
    context_object_name = 'youngpeople'

    def get_queryset(self):
        return get_high_risk_cases().annotate(
            offence_count=Count('offences')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = get_dashboard_stats()
        return context


class CourtHearingCreateView(LoginRequiredMixin, CreateView):
    model = CourtHearing
    template_name = 'justice/courthearing_form.html'
    fields = [
        'young_person', 'hearing_date', 'court_name',
        'outcome', 'presiding_judge'
    ]
    success_url = reverse_lazy('justice:youngperson-list')


class CourtHearingDetailView(LoginRequiredMixin, DetailView):
    model = CourtHearing
    template_name = 'justice/courthearing_detail.html'
    context_object_name = 'hearing'


class CaseWorkerCreateView(LoginRequiredMixin, CreateView):
    model = CaseWorker
    template_name = 'justice/caseworker_form.html'
    fields = ['user', 'employee_id', 'phone', 'department']
    success_url = reverse_lazy('justice:youngperson-list')


class StatsDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        stats = get_dashboard_stats()
        return render(request, 'justice/stats.html', {'stats': stats})
    
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        stats = get_dashboard_stats()
        return render(request, 'justice/home.html', {'stats': stats})