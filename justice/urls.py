from django.urls import path
from . import views

app_name = 'justice'

urlpatterns = [
    path('', views.YoungPersonListView.as_view(), name='home'),
    path('youngperson/', views.YoungPersonListView.as_view(), name='youngperson-list'),
    path('youngperson/<int:pk>/', views.YoungPersonDetailView.as_view(), name='youngperson-detail'),
    path('youngperson/create/', views.YoungPersonCreateView.as_view(), name='youngperson-create'),
    path('offence/create/', views.OffenceCreateView.as_view(), name='offence-create'),
    path('intervention/create/', views.InterventionCreateView.as_view(), name='intervention-create'),
    path('intervention/<int:pk>/update/', views.InterventionUpdateView.as_view(), name='intervention-update'),
    path('dashboard/', views.CaseWorkerDashboardView.as_view(), name='dashboard'),
    path('caseworker/create/', views.CaseWorkerCreateView.as_view(), name='caseworker-create'),
    path('courthearing/create/', views.CourtHearingCreateView.as_view(), name='courthearing-create'),
    path('intervention/', views.InterventionListView.as_view(), name='intervention-list'),
    path('courthearing/<int:pk>/', views.CourtHearingDetailView.as_view(), name='courthearing-detail'),
]