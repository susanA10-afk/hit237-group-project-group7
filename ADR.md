# Architecture Decision Records
## HIT237 — Youth Justice & Crime App — Group 7

This document records all the major design decisions we made 
while building this Django application. We update it as we go, 
and each decision links back to the actual code so markers can 
see where it was implemented.

---

## ADR-001: How we structured our Django apps

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
When we started building, we had to decide how to split the 
project into Django apps. We had two clearly different parts 
of the system — the internal case management side and the 
project settings and routing. We needed a structure that kept 
things organised and easy to work on separately.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Put everything in one app | Simple to set up | Gets messy fast, hard to maintain |
| One app per model | Very separated | Way too complicated for our project |
| Two apps — justice and youthjustice | Clean, manageable, easy to understand | Needs careful URL management |

### What we decided
We went with two apps:
- `justice/` handles all the case management — young persons, 
caseworkers, offences, interventions, court hearings
- `youthjustice/` handles project-level settings and URL routing

This follows Django's loose coupling philosophy — each app 
does one thing and can be understood on its own without 
needing to read the whole project.

**Code reference:** `youthjustice/settings.py` — INSTALLED_APPS 
lists justice as a registered app

### What this means going forward
- Each app has its own models, views, urls and templates
- Apps can be changed without breaking each other
- New apps can be added cleanly if needed

---

## ADR-002: Using a through model for CourtHearing and Offence

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
A court hearing can involve more than one offence, and the 
same offence can come up in multiple hearings. This is a 
many-to-many relationship. We had to decide the best way 
to model this in Django.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Simple ManyToManyField | Less code to write | Cannot store extra info about the connection |
| Through model — HearingOffence | Can store charge type for each offence in each hearing | Slightly more code |

### What we decided
We used a through model called `HearingOffence` that sits 
between `CourtHearing` and `Offence`. It has an extra field 
called `charge_type` which records what the person was 
actually charged with in that specific hearing.

This makes sense because charge type belongs to the 
relationship between a hearing and an offence — not to 
either one on its own.

**Code reference:** `justice/models.py` — HearingOffence class lines 99–105

### What this means going forward
- We can record richer data about each hearing
- Adding offences to hearings needs to go through 
HearingOffence rather than directly
- Satisfies the Django ORM relationship requirements 
for this assessment

---

## ADR-003: Using class-based views instead of function-based views

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
Django gives you two ways to write views — function-based 
views (FBVs) and class-based views (CBVs). We had to pick 
one consistent approach for the whole project.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Function-based views | Easy to read, very explicit | Lots of repeated code for basic list/detail/create pages |
| Class-based views | Much less code, built-in CRUD support, reusable | Takes more time to learn how they work |

### What we decided
We use Django's built-in class-based views throughout the 
project — ListView, DetailView, CreateView, UpdateView and 
DeleteView. This follows the DRY principle (Don't Repeat 
Yourself) because we get standard CRUD functionality without 
writing the same logic over and over.

**Code reference:** `justice/views.py` —
- YoungPersonListView lines 13–30
- YoungPersonDetailView lines 33–41
- YoungPersonCreateView lines 44–51
- OffenceCreateView lines 54–61
- InterventionCreateView lines 64–71
- InterventionUpdateView lines 74–78
- CaseWorkerDashboardView lines 81–89

`justice/urls.py` — urlpatterns lines 6–15

### What this means going forward
- All views follow the same consistent pattern
- Much less boilerplate code across the project
- Team members need to understand how Django CBVs work 
internally

---

## ADR-004: Extending Django's built-in User model

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
We needed caseworkers to be able to log in to the system. 
We also needed to store extra information about them like 
their employee ID, phone number, and department. We had 
to decide how to handle user accounts.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Build a completely custom user system | Full control over everything | Huge amount of work, risky to get wrong |
| Use Django User model as-is | Simplest option | Cannot add custom fields like employee ID |
| Extend with OneToOneField (what we did) | Keeps Django auth working, lets us add custom fields | Two linked models to manage |

### What we decided
We extend Django's built-in User model by linking it to our 
`CaseWorker` model using a OneToOneField. This means we keep 
all of Django's login, logout and permissions system working 
out of the box, while still being able to store the extra 
caseworker-specific information we need.

This follows Django's reusability philosophy — we reuse 
what Django already gives us rather than rebuilding it 
from scratch.

**Code reference:** `justice/models.py` — CaseWorker class, 
OneToOneField linking to Django's User model

### What this means going forward
- Django admin login works automatically
- Password handling and sessions are managed by Django
- When creating a new caseworker we also need to create 
a linked User account

---

## ADR-005: QuerySet design choices

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
When fetching data from the database we had to decide how 
to write our QuerySets efficiently. Poorly written queries 
can cause the N+1 problem where Django makes hundreds of 
separate database calls instead of one.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Basic QuerySet without optimisation | Simple to write | Slow, hits database too many times |
| select_related for foreign keys | Fetches related data in one SQL JOIN | Only works for ForeignKey and OneToOne |
| prefetch_related for many-to-many | Fetches related sets efficiently | Slightly more complex |

### What we decided
We use `select_related` when fetching models that have 
ForeignKey relationships — for example fetching a list 
of offences and needing the related young person in the 
same query. We use `prefetch_related` for many-to-many 
relationships like fetching young persons with their 
caseworkers.

This follows Django's explicit is better than implicit 
philosophy — we are deliberate about how data is fetched 
rather than letting Django make many small queries by default.

**Code reference:** `justice/views.py` —
- YoungPersonListView.get_queryset lines 19–30 — uses 
select_related and prefetch_related with annotate for 
offence count
- YoungPersonDetailView.get_queryset lines 38–41 — uses 
prefetch_related to fetch offences, interventions and 
hearings in one query
- CaseWorkerDashboardView.get_queryset lines 86–89 — uses 
high_risk custom manager with prefetch_related and annotate

### What this means going forward
- Fewer database queries means faster page loads
- QuerySet optimisation needs to be considered whenever 
a new view is added

---

*This document will keep being updated as development 
continues. Line number references will be added once 
all views and models are finalised.*

---

## ADR-006: Custom Manager for high risk young persons

**Status:** Accepted  
**Date:** April 2026  
**Author:** Susan Acharya

### What was the problem
The caseworker dashboard needs to show only high risk young 
persons. We could filter in every view individually but that 
would repeat the same filter logic in multiple places.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Filter in every view manually | Simple to write | Repeats same logic everywhere, violates DRY |
| Custom manager on YoungPerson model | One place to define the filter, reusable everywhere | Slightly more setup |

### What we decided
We created a custom manager called `high_risk` on the 
YoungPerson model. Any view can access high risk young 
persons by simply calling `YoungPerson.high_risk.all()` 
without repeating filter logic anywhere.

This follows Django's DRY philosophy — the filtering 
logic is defined once and reused everywhere it is needed.

**Code reference:** 
- `justice/models.py` — high_risk custom manager
- `justice/views.py` — CaseWorkerDashboardView.get_queryset 
line 87 uses YoungPerson.high_risk.prefetch_related()

### What this means going forward
- Any new view can reuse the high_risk manager easily
- Filter logic only needs to be changed in one place
- Makes the codebase cleaner and easier to read

---

*This document will keep being updated as development 
continues.*