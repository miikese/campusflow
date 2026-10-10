# Engineer B feature group

AI-authored code and tests, organized for study and review. This document does
not claim that a fellow personally implemented them.

Application: `campusflow/workflow.py` and `campusflow/reports.py`.
Tests: `tests/test_workflow.py`.

Responsibilities: nonblank assignment; resolved-ticket protection; strict
status transitions; explicit reopening; open-only queue; complete reports.

Read `update_status` first: normalize the requested status, reject resolved
records and invalid transitions, check assignment, then mutate. Every check
comes before the assignment to status. Reopening is a separate operation.

The queue filters open records, then sorts by `(priority_rank, numeric_id)`.
Reports count all records, including resolved tickets, rather than just the
queue. Their status and priority subtotals each equal the collection size.

Run this feature group's tests from the root:

```sh
python3 -m unittest tests.test_workflow -v
```

For your defence, explain why in_progress is excluded from this queue, why
T002 precedes T1000, which transitions are invalid, what reopening preserves,
and how an empty report works. Record only your real experiments and reviews.
