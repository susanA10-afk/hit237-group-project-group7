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

**Diagram reference:** 
- `youthjustice/docs/ERD.md` — full entity relationship diagram
- `youthjustice/docs/ClassDiagram.md` — class diagram

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

**Status:** Superseded by ADR-008 
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

### Why this was superseded
When Assessment 4 introduced role-based access control, this
approach broke down. The role lived on CaseWorker, not on the
user object itself. Every permission check had to join two
models — authenticate via User, then look up CaseWorker to
find the role. LoginRequiredMixin and view-level role checks
became awkward. Django's own documentation recommends defining
a custom user model at the start of a project. We should have
done this from the beginning.

**Superseded by:** ADR-008

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

## ADR-007: Service layer architecture

**Status:** Accepted
**Date:** May 2026
**Author:** Susan Acharya

### What was the problem
In Assessment 2, all business logic lived directly inside view
classes. Views were doing too many things at once — handling HTTP
requests, querying the database, enforcing business rules, and
preparing template context. This made the logic impossible to
test without simulating a full HTTP request, and it made views
hard to read.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Keep logic in views | No extra files | Views become bloated, logic untestable in isolation |
| Fat model approach | Logic close to data | Models become hard to maintain |
| Dedicated service module — services.py | Logic isolated, testable, reusable | Extra layer to understand |
| Class-based services | Very structured | Overkill for this project size |

### What we decided
We created `assessment4/justice/services.py` containing all
business logic as plain Python functions. Views call service
functions rather than touching the database directly.

We chose functions over classes because our operations are
stateless — they take inputs and return outputs without needing
to maintain state between calls.

Key service functions:
- `get_all_young_persons()` — fetches all young persons with related data
- `get_young_person_by_id(person_id)` — raises YoungPersonNotFound if not found
- `record_offence(young_person_id, offence_data)` — records offence inside a transaction, auto-sets risk to high for serious offences
- `assign_intervention(young_person_id, caseworker, intervention_data)` — enforces max 3 active interventions limit
- `get_dashboard_stats()` — aggregates counts across all models

**Code reference:**
- `assessment4/justice/services.py` — all service functions
- `assessment4/justice/views.py` — views import and call services
- `assessment4/justice/tests.py` — RecordOffenceServiceTest, InterventionLimitTest

### What this means going forward
- Views only handle HTTP — no business logic in view classes
- Service functions can be unit tested without simulating HTTP requests
- Business rules are in one place and reused across multiple views

---

## ADR-008: Custom User model with role-based access control

**Status:** Accepted — supersedes ADR-004
**Date:** May 2026
**Author:** Susan Acharya

### What was the problem
ADR-004's OneToOneField approach worked for basic login but
created a structural problem when we introduced roles. The role
lived on CaseWorker, not on the user object itself. Every
permission check required two model lookups. Django's documentation
is clear on this — set a custom user model before the first
migration. We did not do this in Assessment 2, which meant
adding it in Assessment 4 required a migration reset.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Keep OneToOneField from ADR-004 | No migration changes | Role check requires two model lookups, fragile |
| Django Groups and Permissions | Built-in, flexible | Complex setup, overkill for two roles |
| AbstractUser with role field | Role lives on the user object, clean checks | Must set AUTH_USER_MODEL before first migration |
| AbstractBaseUser from scratch | Maximum control | Large amount of boilerplate, high risk |

### What we decided
We created a CustomUser model in a new accounts app by
extending AbstractUser and adding a role field with choices
of admin and caseworker. The default role is caseworker.

Two helper methods make role checks readable anywhere:
- `is_caseworker()` — returns True if role is caseworker
- `is_admin_user()` — returns True if role is admin

AUTH_USER_MODEL = 'accounts.CustomUser' is set in settings
so Django uses this model for all authentication.

**Code reference:**
- `assessment4/accounts/models.py` — CustomUser class, ROLE_CHOICES, helper methods
- `assessment4/youthjustice/settings.py` — AUTH_USER_MODEL
- `assessment4/justice/views.py` — LoginRequiredMixin on all views
- `assessment4/accounts/tests.py` — CustomUserModelTest, AuthenticationTest

### What this means going forward
- Role is always available on the user object with no extra queries
- LoginRequiredMixin enforces authentication at the class level
- Adding a new role only requires a new ROLE_CHOICES entry and a helper method

---

## ADR-009: Custom domain exceptions

**Status:** Accepted
**Date:** May 2026
**Author:** Susan Acharya

### What was the problem
In Assessment 2 there was no custom exception handling. When
something went wrong — a young person ID that did not exist,
an intervention limit breached — Django raised a generic
DoesNotExist error with no domain meaning. The other option
was raising Http404 inside service functions, which would
couple business logic to HTTP concerns.

### Options we looked at

| Option | Good | Bad |
|--------|------|-----|
| Bare DoesNotExist | No extra code | No domain meaning, hard to distinguish error types |
| Http404 in services | Simple | Couples business logic to HTTP, wrong layer |
| Custom exception classes | Named, testable, catchable by views | Small amount of extra code upfront |

### What we decided
We created `assessment4/justice/exceptions.py` with five custom
exception classes, each inheriting from Python's base Exception:

- `YoungPersonNotFound` — raised when a lookup by ID fails
- `InterventionLimitExceeded` — raised when assigning an intervention would exceed the limit of three active per person
- `UnauthorisedAccess` — raised when a user tries to access a case not assigned to them
- `InvalidRiskLevel` — raised when an invalid risk value is provided
- `OffenceNotFound` — raised when an offence record lookup fails

**Code reference:**
- `assessment4/justice/exceptions.py` — all five exception classes
- `assessment4/justice/services.py` — get_young_person_by_id raises YoungPersonNotFound; assign_intervention raises InterventionLimitExceeded
- `assessment4/justice/tests.py` — tests verify exceptions raised correctly

### What this means going forward
- Errors have clear names and can be caught specifically
- Services stay decoupled from HTTP concerns
- New error conditions just need a new exception class

---

## ADR-010: Testing strategy

**Status:** Accepted
**Date:** May 2026
**Author:** Susan Acharya

### What was the problem
Assessment 4 requires a meaningful test suite. We needed to
decide what to test, how to structure tests, and be honest
about what we chose not to test and why. Tests that only check
trivial conditions do not verify real behaviour.

### Structure
- `assessment4/justice/tests.py` — service functions, business rules, view permissions
- `assessment4/accounts/tests.py` — CustomUser model and authentication

### What we tested and why

| Test area | What it verifies | Why it matters |
|-----------|-----------------|----------------|
| YoungPersonModelTest | Age calculation and is_high_risk() | Core model behaviour — if wrong, downstream logic breaks |
| RecordOffenceServiceTest | Serious offences auto-set risk to high | Silent bug here produces wrong risk data |
| GetYoungPersonServiceTest | YoungPersonNotFound raised for missing ID | If it returns None silently, callers break |
| InterventionLimitTest | Raises InterventionLimitExceeded at limit of 3 | Hard business rule — must be enforced |
| DashboardStatsTest | Counts aggregate correctly | Statistics shown to admins must be accurate |
| LoginRequiredTest | Unauthenticated requests get 302 redirect | If this fails, all data is exposed |
| CustomUserModelTest | Role defaults to caseworker, helper methods correct | Everything else depends on this working |
| AuthenticationTest | Login works with valid credentials, fails with wrong | Login is the entry point to the whole app |

**Total: 30 tests, all passing**

### What we chose not to test and why

| Area | Reason |
|------|--------|
| Template HTML output | Couples tests to presentation — any styling change breaks tests |
| Django admin interface | Django tests its own admin already |
| Database migrations | Verified by running the server, not our logic to test |

**Code reference:**
- `assessment4/justice/tests.py`
- `assessment4/accounts/tests.py`
- `assessment4/evidence/` — screenshots of 30 tests passing

### What this means going forward
- New service functions need corresponding tests
- Permission boundaries always need a LoginRequiredTest check
- Run with `python manage.py test`

---

## ADR-011: Feature growth from Assessment 2 to Assessment 4

**Status:** Accepted
**Date:** May 2026
**Author:** Susan Acharya

### What was the problem
Assessment 4 required demonstrating real improvement in
application functionality. We needed to document what changed
and why those changes reflect genuine architectural maturity
rather than surface-level additions.

### What the application could do after Assessment 2
- List, view, and create young persons, offences, interventions, and court hearings
- Dashboard showing high risk cases
- No authentication — any visitor could access all data
- Business logic mixed into view classes with no separation

### What was added in Assessment 4

| Feature | What it changes |
|---------|----------------|
| User authentication via CustomUser | Application is now secure — data sits behind login |
| Role-based access (admin/caseworker) | Users see what their role allows, nothing more |
| Service layer in services.py | Business logic is isolated and independently testable |
| Custom exceptions in exceptions.py | Errors are named and handled at the correct layer |
| Intervention limit enforcement | System rejects a fourth active intervention rather than silently allowing it |
| Automatic risk escalation | Recording a serious offence sets risk level to high without manual input |
| Statistics dashboard (admin only) | Admins see aggregate counts across all models |
| Full CRUD for all entities | Create, update, delete for all models |

**Code reference:**
- `assessment4/accounts/models.py` — CustomUser
- `assessment4/justice/services.py` — all service functions
- `assessment4/justice/exceptions.py` — domain exceptions
- `assessment4/justice/views.py` — LoginRequiredMixin, role-based access

### What this means going forward
- The application now has a production-grade separation of concerns
- New features are added through the service layer without modifying views directly

---

*ADR last updated: May 2026*
*Assessment 4 additions: ADR-007, ADR-008, ADR-009, ADR-010, ADR-011*
*ADR-004 superseded by ADR-008*