from django.db import transaction
from django.utils import timezone
from .models import YoungPerson, Offence, Intervention, CourtHearing
from .exceptions import (
    YoungPersonNotFound, 
    UnauthorisedAccess,
    InterventionLimitExceeded
)

MAX_ACTIVE_INTERVENTIONS = 3


def get_all_young_persons():
    """
    Returns all young persons with related data.
    Uses select_related and prefetch_related for efficiency.
    """
    return YoungPerson.objects.select_related().prefetch_related(
        'offences', 'interventions', 'caseworkers'
    )


def get_high_risk_cases():
    """
    Returns only high risk young persons.
    Uses custom HighRiskManager.
    """
    return YoungPerson.high_risk.prefetch_related(
        'offences', 'interventions'
    )


def get_young_person_by_id(person_id):
    """
    Returns a single young person by ID.
    Raises YoungPersonNotFound if not found.
    """
    try:
        return YoungPerson.objects.get(pk=person_id)
    except YoungPerson.DoesNotExist:
        raise YoungPersonNotFound(
            f"Young person with id {person_id} not found."
        )


def record_offence(young_person_id, offence_data):
    """
    Records a new offence for a young person.
    Automatically updates risk level if serious offence.
    Uses transaction.atomic() to ensure both operations succeed.
    """
    with transaction.atomic():
        young_person = get_young_person_by_id(young_person_id)
        
        offence = Offence.objects.create(
            young_person=young_person,
            **offence_data
        )
        
        # Automatically update risk level for serious offences
        if offence.severity == 'serious':
            young_person.risk_level = 'high'
            young_person.save()
        
        return offence


def assign_intervention(young_person_id, caseworker, intervention_data):
    """
    Assigns an intervention to a young person.
    Checks intervention limit before creating.
    Uses transaction.atomic() for safety.
    """
    with transaction.atomic():
        young_person = get_young_person_by_id(young_person_id)
        
        active_count = Intervention.objects.filter(
            young_person=young_person,
            status='active'
        ).count()
        
        if active_count >= MAX_ACTIVE_INTERVENTIONS:
            raise InterventionLimitExceeded(
                f"{young_person} already has {MAX_ACTIVE_INTERVENTIONS} "
                f"active interventions."
            )
        
        return Intervention.objects.create(
            young_person=young_person,
            assigned_worker=caseworker,
            **intervention_data
        )


def get_dashboard_stats():
    """
    Returns statistics for the admin dashboard.
    Aggregates data across multiple models.
    """
    from django.db.models import Count
    
    return {
        'total_young_persons': YoungPerson.objects.count(),
        'high_risk_count': YoungPerson.high_risk.count(),
        'total_offences': Offence.objects.count(),
        'active_interventions': Intervention.objects.filter(
            status='active'
        ).count(),
        'total_hearings': CourtHearing.objects.count(),
    }