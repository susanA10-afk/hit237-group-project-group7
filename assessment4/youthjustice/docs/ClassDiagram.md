# Relationship

CustomUser → CaseWorker  
- One CustomUser has one CaseWorker profile (One-to-One)

CaseWorker → YoungPerson  
- One CaseWorker manages many YoungPersons (One-to-Many)

YoungPerson → Offence  
- One YoungPerson can commit many Offences (One-to-Many)

YoungPerson → Intervention  
- One YoungPerson can receive many Interventions (One-to-Many)

YoungPerson → CourtHearing  
- One YoungPerson can attend many CourtHearings (One-to-Many)

CourtHearing ↔ Offence (via HearingOffence)  
- Many-to-Many relationship through HearingOffence junction table

Views → Services → Models  
- Views interact with the service layer which handles business logic and database operations

Services → Exceptions  
- Services raise custom exceptions for validation and error handling

# Diagram

```mermaid
classDiagram

class CustomUser {
  +int id
  +string username
  +string email
  +string password
  +string role
}

class CaseWorker {
  +int id
  +string employee_id
  +string phone
  +string department
  +__str__()
}

class YoungPerson {
  +int id
  +string first_name
  +string last_name
  +date date_of_birth
  +string gender
  +string postcode
  +string risk_level
  +age()
  +is_high_risk()
  +__str__()
}

class Offence {
  +int id
  +string offence_type
  +date date_of_offence
  +string location
  +string severity
  +string description
  +__str__()
}

class Intervention {
  +int id
  +string intervention_type
  +date start_date
  +date end_date
  +string status
  +string outcome
  +__str__()
}

class CourtHearing {
  +int id
  +date hearing_date
  +string court_name
  +string outcome
  +string presiding_judge
  +__str__()
}

class HearingOffence {
  +int id
  +string charge_type
  +__str__()
}

class HighRiskManager {
  +get_queryset()
}

class JusticeService {
  +create_intervention()
  +assign_caseworker()
  +generate_statistics()
  +validate_young_person()
}

class AuthenticationService {
  +authenticate_user()
  +login_user()
  +logout_user()
}

class ServiceError {
  +message
}

class ValidationError {
  +message
}

class AuthenticationError {
  +message
}

CustomUser --> CaseWorker

CaseWorker --> YoungPerson

YoungPerson --> Offence
YoungPerson --> Intervention
YoungPerson --> CourtHearing

CourtHearing --> HearingOffence
Offence --> HearingOffence

JusticeService --> YoungPerson
JusticeService --> Intervention
JusticeService --> ServiceError
JusticeService --> ValidationError

AuthenticationService --> CustomUser
AuthenticationService --> AuthenticationError
```