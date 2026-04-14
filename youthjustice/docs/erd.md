# Entity Relationship Diagram

```mermaid
erDiagram

    USER ||--|| CASEWORKER : has
    CASEWORKER ||--o{ YOUNGPERSON : manages

    YOUNGPERSON ||--o{ OFFENCE : commits
    YOUNGPERSON ||--o{ INTERVENTION : receives
    YOUNGPERSON ||--o{ COURTHEARING : attends

    COURTHEARING ||--o{ HEARINGOFFENCE : includes
    OFFENCE ||--o{ HEARINGOFFENCE : linked_to

    USER {
        int id
        string username
        string email
    }

    CASEWORKER {
        int id
        int user_id
        string employee_id
        string phone
        string department
    }

    YOUNGPERSON {
        int id
        string first_name
        string last_name
        date date_of_birth
        string gender
        string postcode
        string risk_level
    }

    OFFENCE {
        int id
        int young_person_id
        string offence_type
        date date_of_offence
        string location
        string severity
        string description
    }

    INTERVENTION {
        int id
        int young_person_id
        int assigned_worker_id
        string intervention_type
        date start_date
        date end_date
        string status
        string outcome
    }

    COURTHEARING {
        int id
        int young_person_id
        date hearing_date
        string court_name
        string outcome
        string presiding_judge
    }

    HEARINGOFFENCE {
        int id
        int hearing_id
        int offence_id
        string charge_type
    }