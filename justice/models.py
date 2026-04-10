from django.db import models
from django.contrib.auth.models import User


class CaseWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class YoungPerson(models.Model):
    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES)
    caseworkers = models.ManyToManyField(CaseWorker, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year


class Offence(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('serious', 'Serious'),
    ]
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name='offences')
    offence_type = models.CharField(max_length=100)
    date_of_offence = models.DateField()
    location = models.CharField(max_length=200)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f"{self.offence_type} - {self.young_person}"


class Intervention(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    ]
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name='interventions')
    assigned_worker = models.ForeignKey(
        CaseWorker, on_delete=models.SET_NULL, null=True)
    intervention_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    outcome = models.TextField(blank=True)

    def __str__(self):
        return f"{self.intervention_type} - {self.young_person}"


class CourtHearing(models.Model):
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name='hearings')
    hearing_date = models.DateTimeField()
    court_name = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)
    presiding_judge = models.CharField(max_length=100)
    offences = models.ManyToManyField(
        Offence, through='HearingOffence', blank=True)

    def __str__(self):
        return f"Hearing for {self.young_person} on {self.hearing_date}"


class HearingOffence(models.Model):
    hearing = models.ForeignKey(CourtHearing, on_delete=models.CASCADE)
    offence = models.ForeignKey(Offence, on_delete=models.CASCADE)
    charge_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.charge_type} - {self.hearing}"