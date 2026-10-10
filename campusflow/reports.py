"""Engineer B feature group: complete status and priority reports (AI-authored)."""

from .tickets import PRIORITIES, STATUSES


def generate_report(tickets):
    return {
        "total": len(tickets),
        "by_status": {status: sum(t["status"] == status for t in tickets) for status in STATUSES},
        "by_priority": {priority: sum(t["priority"] == priority for t in tickets) for priority in PRIORITIES},
    }

