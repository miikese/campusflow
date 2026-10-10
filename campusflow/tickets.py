"""Engineer A feature group: creation, validation, priority and lookup.

AI-authored implementation; this is not evidence of a fellow's independent work.
"""

import re


CATEGORIES = ("Network", "Hardware", "Software", "Other")
URGENCIES = ("low", "medium", "high")
PRIORITIES = ("critical", "high", "medium", "low")
STATUSES = ("open", "in_progress", "resolved")
FIELDS = {
    "id", "title", "category", "urgency", "affected_users",
    "priority", "status", "assigned_to",
}


def nonblank(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text.")
    return value.strip()


def normalize_choice(value, choices, field):
    text = nonblank(value, field).casefold()
    for choice in choices:
        if text == choice.casefold():
            return choice
    raise ValueError(f"{field} must be one of: {', '.join(choices)}.")


def validate_affected_users(value):
    if type(value) is not int or value <= 0:
        raise ValueError("Affected users must be a positive integer (not a Boolean or decimal).")
    return value


def ticket_number(ticket_id):
    text = nonblank(ticket_id, "Ticket ID").upper()
    if not re.fullmatch(r"T[0-9]{3,}", text):
        raise ValueError("Ticket ID must look like T001.")
    number = int(text[1:])
    if number < 1 or text != f"T{number:03d}":
        raise ValueError("Ticket ID must have a positive, consistently padded number, such as T001.")
    return number


def calculate_priority(urgency, affected_users):
    """Apply the four ordered rules; validate independently of the CLI."""
    urgency = normalize_choice(urgency, URGENCIES, "Urgency")
    validate_affected_users(affected_users)
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Append only after validation succeeds, returning an independent copy."""
    title = nonblank(title, "Title")
    category = normalize_choice(category, CATEGORIES, "Category")
    urgency = normalize_choice(urgency, URGENCIES, "Urgency")
    priority = calculate_priority(urgency, affected_users)
    next_number = max((ticket_number(ticket["id"]) for ticket in tickets), default=0) + 1
    ticket = {
        "id": f"T{next_number:03d}",
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket.copy()


def _find_record(tickets, ticket_id):
    """Internal mutable lookup, used by workflow after validation."""
    number = ticket_number(ticket_id)
    normalized_id = f"T{number:03d}"
    for ticket in tickets:
        if ticket["id"] == normalized_id:
            return ticket
    raise ValueError(f"Unknown ticket ID: {normalized_id}.")


def find_ticket(tickets, ticket_id):
    return _find_record(tickets, ticket_id).copy()


def list_tickets(tickets):
    return [ticket.copy() for ticket in tickets]


def validate_records(tickets):
    """Reject malformed or inconsistent persisted data before using it."""
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON array.")
    seen_ids = set()
    for index, ticket in enumerate(tickets, start=1):
        try:
            if not isinstance(ticket, dict) or set(ticket) != FIELDS:
                raise ValueError("Each ticket must contain exactly the eight required fields.")
            number = ticket_number(ticket["id"])
            if ticket["id"] != f"T{number:03d}" or number in seen_ids:
                raise ValueError("Ticket IDs must be normalized and unique.")
            seen_ids.add(number)
            if nonblank(ticket["title"], "Title") != ticket["title"]:
                raise ValueError("Stored titles must be trimmed.")
            for field, choices in (("category", CATEGORIES), ("urgency", URGENCIES),
                                   ("priority", PRIORITIES), ("status", STATUSES)):
                if normalize_choice(ticket[field], choices, field) != ticket[field]:
                    raise ValueError(f"Stored {field} must be normalized.")
            expected = calculate_priority(ticket["urgency"], ticket["affected_users"])
            if ticket["priority"] != expected:
                raise ValueError("Stored priority does not match urgency and affected users.")
            staff = ticket["assigned_to"]
            if staff is not None and nonblank(staff, "Staff name") != staff:
                raise ValueError("Stored staff names must be trimmed.")
            if ticket["status"] != "open" and staff is None:
                raise ValueError("An in_progress or resolved ticket must be assigned.")
        except ValueError as error:
            raise ValueError(f"Invalid ticket record {index}: {error}") from error
    return tickets

