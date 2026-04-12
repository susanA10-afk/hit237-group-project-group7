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

**Code reference:** `youthjustice/settings.py` INSTALLED_APPS — 
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
| Through mode