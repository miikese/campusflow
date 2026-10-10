# Implemented design decisions

These describe the actual AI-authored implementation. They are not agreements
made on behalf of either fellow. Both engineers must understand, discuss and
record their own approval or changes before claiming team planning evidence.

| Decision | Implemented behavior |
| --- | --- |
| Ticket records | An in-memory list of dictionaries with exactly the eight required fields |
| Collection passing | Every business function receives the list explicitly; no mutable module global |
| Invalid input | Business functions raise ValueError; StorageError subclasses ValueError; CLI displays errors |
| Return values | Queries and mutators return shallow copies of records; queue/list return copied lists; report returns counts |
| Persistence | campusflow/storage.py handles JSON and accepts str/Path paths |
| Test isolation | Direct function tests and CLI subprocesses; persistence tests use temporary directories |
| Integration | main.py owns the collection and invokes both feature groups; input stays outside business logic |
| Organization | A: tickets and matching tests; B: workflow/reports and matching tests; shared: storage, CLI and demo |
| IDs after reload | Validate normalized unique IDs; allocate highest numeric suffix + 1, padded to at least three digits |
| Limitations | One process per file; no locking, database, dependencies, GUI or AI runtime |

Copies protect stored records from accidental edits through function results.
A shallow copy is sufficient because all eight fields contain scalar values.
Internal `_find_record` supplies mutable records only to workflow functions.
All validation occurs before a record/list is changed. `type(value) is int`
rejects Booleans, which are subclasses of integers in Python.

## Actual function contracts

```python
# Engineer A: campusflow/tickets.py
calculate_priority(urgency, affected_users) -> str
create_ticket(tickets, title, category, urgency, affected_users) -> dict
find_ticket(tickets, ticket_id) -> dict
list_tickets(tickets) -> list
validate_records(tickets) -> list

# Engineer B: campusflow/workflow.py
assign_ticket(tickets, ticket_id, staff_name) -> dict
update_status(tickets, ticket_id, new_status) -> dict
reopen_ticket(tickets, ticket_id) -> dict
work_queue(tickets) -> list

# Engineer B: campusflow/reports.py
generate_report(tickets) -> dict  # total, by_status, by_priority

# Shared: campusflow/storage.py
load_tickets(path) -> list
save_tickets(tickets, path) -> None
```

## Exact transitions

| Current status | Operation | Result / prerequisite |
| --- | --- | --- |
| open | update to in_progress | Allowed only when assigned |
| in_progress | update to resolved | Allowed |
| resolved | explicitly reopen | open, retaining assignment |
| Any other combination | update / reopen | Reject without mutation |

Assignment changes are allowed when open or in_progress. Resolved tickets
require explicit reopening first. No same-status no-op or extra transition
has been added. The assessment's queue filters exactly status == open.

## Persistence

Loaded JSON must be an array. Validate exact field names, types, positive
counts, canonical enum values, unique normalized IDs, computed priority,
trimmed nonblank titles/staff and assignment for progressed/resolved records.
Reject duplicate JSON object keys. Input normalization is allowed at the
business-function boundary; persisted records are required to be normalized.

A load error stops CLI startup with exit status 1. Saving also revalidates the
existing file so damaged data discovered after startup cannot be overwritten.
Valid concurrent changes are not reconciled; this is explicitly single-process.

Safe saving validates, serializes UTF-8 JSON, creates parent directories,
writes a temporary sibling, flushes/fsyncs it and calls os.replace. Failed
replacement leaves the original file intact and removes the temporary file.

Option 9 saves explicitly. Option 0, EOF and Ctrl+C save completed pending
changes. Read-only sessions do not create an empty file. Failed saves retain
changes while the menu remains available; input ending with a failed save
returns exit status 1. Default storage is anchored to the project root.

## Evidence and pending human decisions

The test suite verifies these behaviors; see test-output.txt. No fellow names,
independent work or teammate approval are recorded. Human agreements and
changes should be added with actual names and real commit/review references.
