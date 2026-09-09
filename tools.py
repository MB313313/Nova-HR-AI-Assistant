"""Mocked HR tools used by Lara via LangChain tool calling."""

from __future__ import annotations

import re
from typing import Any

from langchain_core.tools import tool

EMPLOYEE_ID_PATTERN = re.compile(r"^E\d{5}$", re.IGNORECASE)

EMPLOYEES: dict[str, dict[str, Any]] = {
    "E12345": {
        "employee_id": "E12345",
        "name": "Amira Nasser",
        "department": "Engineering",
        "role": "Software Engineer",
        "email": "amira.nasser@nova-labs.com",
        "location": "Cairo",
        "manager": "Omar Farouk",
        "start_date": "2022-03-14",
    },
    "E10001": {
        "employee_id": "E10001",
        "name": "Omar Farouk",
        "department": "Engineering",
        "role": "Engineering Manager",
        "email": "omar.farouk@nova-labs.com",
        "location": "Cairo",
        "manager": "Layla Hassan",
        "start_date": "2019-06-01",
    },
    "E20010": {
        "employee_id": "E20010",
        "name": "Sara Adel",
        "department": "Data",
        "role": "Data Scientist",
        "email": "sara.adel@nova-labs.com",
        "location": "Dubai",
        "manager": "Omar Farouk",
        "start_date": "2023-01-09",
    },
    "E30022": {
        "employee_id": "E30022",
        "name": "Youssef Kamal",
        "department": "Human Resources",
        "role": "HR Specialist",
        "email": "youssef.kamal@nova-labs.com",
        "location": "Cairo",
        "manager": "Layla Hassan",
        "start_date": "2021-11-22",
    },
    "E40015": {
        "employee_id": "E40015",
        "name": "Nour El-Sayed",
        "department": "Product",
        "role": "Product Manager",
        "email": "nour.elsayed@nova-labs.com",
        "location": "Riyadh",
        "manager": "Layla Hassan",
        "start_date": "2020-08-17",
    },
}

LEAVE_BALANCES: dict[str, dict[str, Any]] = {
    "E12345": {"annual": 8, "sick": 3, "personal": 1},
    "E10001": {"annual": 8, "sick": 5, "personal": 1},
    "E20010": {"annual": 15, "sick": 8, "personal": 3},
    "E30022": {"annual": 10, "sick": 6, "personal": 2},
    "E40015": {"annual": 4, "sick": 3, "personal": 0},
}

INTERVIEW_QUESTIONS: dict[str, list[str]] = {
    "data scientist": [
        "How do you decide between a linear model and a tree-based model for a tabular problem?",
        "Explain bias-variance tradeoff with a hiring-prediction example.",
        "How would you detect and mitigate data leakage in a production ML pipeline?",
        "Walk through how you would evaluate a classification model when the classes are imbalanced.",
        "How do you explain a model's prediction to a non-technical stakeholder?",
        "Describe an experiment you would run to measure the impact of a new ranking feature.",
    ],
    "software engineer": [
        "What is object-oriented programming, and when would you choose composition over inheritance?",
        "Explain the difference between REST and GraphQL, and when you would use each.",
        "How would you design a rate limiter for an internal HR API?",
        "What is the difference between a process and a thread? How does that affect debugging?",
        "How do you approach writing tests for a function that calls an external service?",
        "Describe how you would roll out a breaking API change with zero downtime.",
    ],
    "product manager": [
        "How do you prioritize a backlog when engineering capacity is limited?",
        "Describe how you would define success metrics for a new employee self-service portal.",
        "How do you handle conflicting requests from Sales and Customer Success?",
        "Walk through a product discovery process you would use for an HR chatbot.",
        "How would you decide whether to build, buy, or partner for an ATS integration?",
    ],
    "hr specialist": [
        "How would you handle an employee complaint about their manager?",
        "What questions are inappropriate to ask in an interview, and why?",
        "How do you explain a performance-improvement plan in a constructive way?",
        "Describe how you would run a fair calibration session for promotions.",
        "What data would you look at to diagnose a spike in attrition?",
    ],
    "engineering manager": [
        "How do you balance delivery pressure with team health?",
        "Describe how you would coach an engineer who is technically strong but misses deadlines.",
        "How do you run a hiring loop that reduces bias?",
        "What signals tell you a team is overloaded?",
        "How would you introduce on-call without burning people out?",
    ],
}

POLICIES: dict[str, dict[str, str]] = {
    "remote_work": {
        "title": "Remote Work Policy",
        "summary": (
            "Nova Labs supports a hybrid model. Employees may work remotely up to 3 days "
            "per week with manager approval. Core collaboration hours are 11:00–16:00 "
            "in the employee's local timezone. Fully remote arrangements require VP approval "
            "and a documented home-office setup. Company equipment must be used for work "
            "systems; personal devices need MDM enrollment."
        ),
    },
    "leave": {
        "title": "Leave Policy",
        "summary": (
            "Full-time employees receive 21 days of annual leave, 10 sick days, and 3 "
            "personal days each calendar year. Leave is requested in the HR portal at least "
            "5 business days in advance for annual leave (except emergencies). Unused annual "
            "leave up to 5 days may roll over to Q1 of the next year. Parental leave is 12 "
            "weeks paid. Public holidays follow the employee's contracted country calendar."
        ),
    },
    "salary": {
        "title": "Salary & Compensation Policy",
        "summary": (
            "Salaries are reviewed annually in March. Off-cycle adjustments require People "
            "Business Partner and Finance approval. Compensation bands are role- and "
            "location-based; managers must not share another employee's pay. Overtime applies "
            "only to eligible non-exempt roles. Bonus eligibility requires being employed on "
            "the payout date. Raise discussions belong in performance reviews, not ad-hoc chat."
        ),
    },
    "benefits": {
        "title": "Benefits Policy",
        "summary": (
            "Benefits include medical insurance from the first day of employment, a wellness "
            "stipend of $600/year, learning budget of $1,000/year, and a retirement match "
            "up to 4%. Enrollment windows are during onboarding and every November. "
            "Dependent coverage can be added within 30 days of a qualifying life event."
        ),
    },
    "dress_code": {
        "title": "Dress Code Policy",
        "summary": (
            "Workplace attire is smart casual in the office. Customer or board-facing meetings "
            "may require business casual. Clothing must be safe for the work environment and "
            "free of offensive messaging. Remote employees should dress professionally for "
            "external video calls."
        ),
    },
    "code_of_conduct": {
        "title": "Code of Conduct",
        "summary": (
            "Employees must treat colleagues with respect, protect confidential employee and "
            "candidate data, avoid conflicts of interest, and report harassment or ethics "
            "concerns to HR or the anonymous ethics line. Retaliation against good-faith "
            "reports is prohibited. Violations may lead to disciplinary action up to termination."
        ),
    },
    "onboarding": {
        "title": "Onboarding Policy",
        "summary": (
            "New hires complete Day-1 orientation, IT access setup, and mandatory compliance "
            "training within 10 business days. Hiring managers assign a buddy and a 30/60/90 "
            "plan. Probation is 90 days, with a written check-in at day 45 and day 90."
        ),
    },
}

_POLICY_ALIASES = {
    "remote": "remote_work",
    "wfh": "remote_work",
    "work from home": "remote_work",
    "hybrid": "remote_work",
    "vacation": "leave",
    "pto": "leave",
    "time off": "leave",
    "sick": "leave",
    "pay": "salary",
    "compensation": "salary",
    "raise": "salary",
    "bonus": "salary",
    "insurance": "benefits",
    "perks": "benefits",
    "attire": "dress_code",
    "clothing": "dress_code",
    "ethics": "code_of_conduct",
    "harassment": "code_of_conduct",
    "conduct": "code_of_conduct",
    "new hire": "onboarding",
    "orientation": "onboarding",
}


def normalize_employee_id(employee_id: str) -> str:
    return (employee_id or "").strip().upper()


def validate_employee_id(employee_id: str) -> str | None:
    normalized = normalize_employee_id(employee_id)
    if not normalized:
        return "employee_id is required."
    if not EMPLOYEE_ID_PATTERN.match(normalized):
        return (
            f"Invalid employee_id '{employee_id}'. "
            "IDs look like E12345 (E followed by 5 digits)."
        )
    return None


def list_employee_directory() -> list[dict[str, str]]:
    return [
        {
            "employee_id": emp["employee_id"],
            "name": emp["name"],
            "role": emp["role"],
            "department": emp["department"],
        }
        for emp in EMPLOYEES.values()
    ]


def get_employee_details(employee_id: str) -> dict:
    """Retrieve an employee's name, department, role, and related profile fields.

    Args:
        employee_id: Unique employee ID such as E12345.
    """
    error = validate_employee_id(employee_id)
    if error:
        return {"error": "invalid_arguments", "message": error}

    record = EMPLOYEES.get(normalize_employee_id(employee_id))
    if not record:
        return {
            "error": "not_found",
            "message": (
                f"No employee found for '{normalize_employee_id(employee_id)}'. "
                "Ask the employee to confirm their ID."
            ),
        }

    return {
        "employee_id": record["employee_id"],
        "name": record["name"],
        "department": record["department"],
        "role": record["role"],
        "email": record["email"],
        "location": record["location"],
        "manager": record["manager"],
        "start_date": record["start_date"],
    }


def check_leave_balance(employee_id: str) -> dict:
    """Return remaining leave balances (annual, sick, personal) for an employee.

    Args:
        employee_id: Unique employee ID such as E12345.
    """
    error = validate_employee_id(employee_id)
    if error:
        return {"error": "invalid_arguments", "message": error}

    employee_id = normalize_employee_id(employee_id)
    if employee_id not in EMPLOYEES:
        return {
            "error": "not_found",
            "message": f"No employee found for '{employee_id}'.",
        }

    balance = LEAVE_BALANCES.get(employee_id)
    if not balance:
        return {
            "error": "not_found",
            "message": f"No leave record found for '{employee_id}'.",
        }

    remaining = int(balance["annual"]) + int(balance["sick"]) + int(balance["personal"])
    return {
        "employee_id": employee_id,
        "name": EMPLOYEES[employee_id]["name"],
        "remaining_leave_days": remaining,
        "breakdown": balance,
    }


def generate_interview_questions(job_role: str) -> list | dict:
    """Generate mocked interview questions for a given job role.

    Args:
        job_role: Role to interview for, e.g. Data Scientist or Software Engineer.
    """
    role = (job_role or "").strip()
    if not role:
        return {"error": "invalid_arguments", "message": "job_role is required."}

    key = role.lower()
    questions = INTERVIEW_QUESTIONS.get(key)
    if questions is None:
        for known_role, known_questions in INTERVIEW_QUESTIONS.items():
            if known_role in key or key in known_role:
                questions = known_questions
                key = known_role
                break

    if questions is None:
        supported = ", ".join(sorted(name.title() for name in INTERVIEW_QUESTIONS))
        return {
            "error": "unsupported_role",
            "message": f"No mocked interview pack for '{role}'. Supported roles: {supported}",
            "job_role": role,
        }

    return questions


def get_company_policy(topic: str) -> dict:
    """Look up a Nova Labs company policy such as remote work, leave, salary, or benefits.

    Args:
        topic: Policy topic, e.g. remote work, salary, leave, dress code, benefits.
    """
    raw = (topic or "").strip()
    if not raw:
        return {
            "error": "invalid_arguments",
            "message": "topic is required.",
            "available_topics": list(POLICIES.keys()),
        }

    needle = raw.lower().replace("-", " ").replace("_", " ")
    policy_key = None
    if needle in POLICIES:
        policy_key = needle
    else:
        compact = needle.replace(" ", "_")
        if compact in POLICIES:
            policy_key = compact
        elif needle in _POLICY_ALIASES:
            policy_key = _POLICY_ALIASES[needle]
        else:
            for alias, mapped in _POLICY_ALIASES.items():
                if alias in needle:
                    policy_key = mapped
                    break
            if policy_key is None:
                for key in POLICIES:
                    if key.replace("_", " ") in needle or needle in key.replace("_", " "):
                        policy_key = key
                        break

    if policy_key is None:
        return {
            "error": "not_found",
            "message": f"No policy matched '{raw}'.",
            "available_topics": [POLICIES[k]["title"] for k in POLICIES],
        }

    policy = POLICIES[policy_key]
    return {
        "topic": policy_key,
        "title": policy["title"],
        "summary": policy["summary"],
    }


HR_TOOLS = [
    tool(get_employee_details),
    tool(check_leave_balance),
    tool(generate_interview_questions),
    tool(get_company_policy),
]

TOOL_REGISTRY = {tool_fn.name: tool_fn for tool_fn in HR_TOOLS}
ALLOWED_TOOL_NAMES = set(TOOL_REGISTRY)
