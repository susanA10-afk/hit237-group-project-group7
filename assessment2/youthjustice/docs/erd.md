# Entity Relationship Diagram
## Youth Justice & Crime App — Group 7

This diagram shows all models in the application and
how they relate to each other.

## Relationships

- User → CaseWorker (one to one)
- CaseWorker ↔ YoungPerson (many to many)
- YoungPerson → Offence (one to many)
- YoungPerson → Intervention (one to many)
- YoungPerson → CourtHearing (one to many)
- CourtHearing ↔ Offence through HearingOffence (through model)

## Diagram

```mermaid
erDiagram
  USER ||--|| CASEWORKER : "extends"
  CASEWORKER }o--o{ YOUNGPERSON : "manages"
  YOUNGPERSON ||--o{ OFFENCE : "has"
  YOUNGPERSON ||--o{ INTERVENTION : "receives"
  YOUNGPERSON ||--o{ COURTHEARING : "attends"
  COURTHEARING ||--o{ HEARINGOFFENCE : "through"
  OFFENCE ||--o{ HEARINGOFFENCE : "through"

  USER {
    int id PK
    string username
    string password
    string email
  }
  CASEWORKER {
    int id PK
    int user_id FK
    string employee_id
    string phone
    string department
  }
  YOUNGPERSON {
    int id PK
    string first_name
    string last_name
    date date_of_birth
    string gender
    string postcode
    string risk_level
  }
  OFFENCE {
    int id PK
    int young_person_id FK
    string offence_type
    date date_of_offence
    string location
    string severity
    text description
  }
  INTERVENTION {
    int id PK
    int young_person_id FK
    int assigned_worker_id FK
    string intervention_type
    date start_date
    date end_date
    string status
    text outcome
  }
  COURTHEARING {
    int id PK
    int young_person_id FK
    datetime hearing_date
    string court_name
    string outcome
    string presiding_judge
  }
  HEARINGOFFENCE {
    int id PK
    int hearing_id FK
    int offence_id FK
    string charge_type
  }
```