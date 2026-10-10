# CampusFlow

A Python command-line campus helpdesk for Wi-Fi outages, faulty laptops,
broken development environments and inaccessible learning platforms.
It creates and prioritizes tickets, assigns staff, enforces a status workflow,
displays the open work queue, generates reports and safely persists JSON.

**Authorship:** The application and tests were generated with AI at the user's
explicit request. Engineer A and B are organizational feature groups; they
are not claims of independent human contributions. The supplied assessment
still requires real fellow contributions, learning experiments and peer reviews.
Names, team ID and partner GitHub username have not been supplied.

## Run locally

Use Python 3.10 or newer. Verified locally with Python 3.12.3. No third-party
packages, database, AI API or runtime network connection are needed.

Open a terminal in this project directory:

```sh
python3 main.py
```

To download the implementation to another computer:

```sh
git clone https://github.com/miikese/campusflow.git
cd campusflow
python3 main.py
```

For this workspace:

```sh
cd /home/student/campus
python3 main.py
```

On Windows, use `py -3 main.py` if `python3` is unavailable. An optional virtual
environment can be created with `python3 -m venv .venv`; there is nothing to install.

Run the repeatable demonstration, using temporary storage:

```sh
python3 main.py --demo
```

Use a separate JSON file for experimentation:

```sh
python3 main.py --data data/practice.json
```

Runtime JSON files should stay private; all `data/*.json` files are ignored
by Git. If you store data elsewhere, add its path to `.gitignore`.

## Menu

| Option | Action |
| --- | --- |
| 1 | Create a ticket; display its ID and calculated priority |
| 2 | List all tickets |
| 3 | View all eight stored fields for one ID |
| 4 | Assign or reassign staff |
| 5 | Move an assigned ticket to in_progress, or an in_progress ticket to resolved |
| 6 | Explicitly reopen a resolved ticket |
| 7 | Display the open-ticket work queue |
| 8 | Show total, three status counts and four priority counts |
| 9 | Save tickets immediately |
| 0 | Save pending changes and exit |

Valid case variations are normalized for categories, urgency, status and ticket
IDs. Titles and staff names are trimmed and must be nonblank. Counts must be
positive integers: zero, negatives, decimals, text and Booleans are rejected.
Failed creations and transitions leave stored records unchanged and do not
consume an ID.

## Priority rules

Rules run in this exact order:

1. High urgency AND at least 10 affected users → critical.
2. High urgency OR at least 10 affected users → high.
3. Medium urgency OR at least 3 affected users → medium.
4. Otherwise → low.

Examples: high + 12 → critical; high + 2 → high; low + 4 → medium;
low + 1 → low. High + 9 is high, while high + 10 is critical.

## Status and queue

Normal lifecycle: `open → in_progress → resolved`. Starting work requires an
assignment. Only explicit reopening changes `resolved → open`; assignment is
retained when reopening. Resolved tickets reject reassignment/status changes
until reopened. Skipping stages, going backwards, and same-status updates are
rejected. Reassignment is allowed while open or in_progress.

The queue includes **only open tickets**. It excludes in_progress and resolved
tickets. Sort order is critical, high, medium, low, then ascending numeric ID:
T002 precedes T010 and T1000. Reports count all stored tickets, including resolved
critical tickets, with zero counts shown when the collection is empty.

## Persistence and recovery

The default file is `data/tickets.json`, relative to the project root even when
the command is launched from another directory. Startup reloads it. A missing
file starts empty; invalid JSON, duplicate IDs/keys, wrong types, invalid records
and inconsistent priorities stop startup with a useful error. Existing data
is not erased or replaced after a load error.

Option 9 saves explicitly. Option 0, EOF and Ctrl+C save pending completed
changes before exiting. An incomplete create operation never adds a partial
record. If saving fails, the menu displays the error and retains changes for
retry; if input also ends and saving still fails, exit status is 1.

Saving validates records and any existing file, writes a temporary file beside
the destination, flushes/fsyncs it and uses atomic replacement. IDs start at
T001 and continue from the highest saved numeric ID, including gaps and T1000+.

To start fresh, close the application and **move** `data/tickets.json` to a backup
location before restarting. To recover malformed data, restore a valid backup
or choose a different `--data` path; the app will not silently reset damaged data.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

49 meaningful tests passed locally, covering all ten required acceptance
scenarios, priority boundaries, invalid types, failed-operation state
preservation, numeric queue ordering, reports, JSON round-trip, safe-write
failure, corrupted data, real CLI subprocesses and restart ID allocation.
See [actual test output](docs/test-output.txt) and [actual demo output](docs/demo-output.txt).
GitHub Actions runs unittest and syntax checks on pushes and PRs.

For commands per feature group, exact manual inputs and expected results,
follow [the testing guide](docs/testing-guide.md).

## Organized feature groups

| Group | Application modules | Matching tests | Human name |
| --- | --- | --- | --- |
| Engineer A | `campusflow/tickets.py`: creation, validation, priority, list/view | `tests/test_tickets.py` | Not supplied |
| Engineer B | `campusflow/workflow.py`, `campusflow/reports.py`: assignment, status, reopening, queue, reports | `tests/test_workflow.py` | Not supplied |
| Shared | `campusflow/storage.py`, `main.py`, demo and integration | `tests/test_storage.py`, `tests/test_cli.py` | Not supplied |

See [Engineer A walkthrough](docs/engineer-a.md), [Engineer B walkthrough](docs/engineer-b.md),
[design decisions](docs/design-decisions.md), [issue drafts](docs/issues.md),
[learning prompts](docs/learning-start.md), and [learning-log templates](docs/ai-learning-log.md).
Both groups were AI-authored; human ownership must be confirmed and evidenced.

## GitHub and submission

The shared repository is [miikese/campusflow](https://github.com/miikese/campusflow).
The complete application is published on `main` at the repository owner's request,
so its code, tests, documentation and source comments are visible on the repository home page.
The original implementation branch is `feat/1-campusflow-helpdesk`.
Human peer-review evidence remains outstanding.
[Implementation PR #8](https://github.com/miikese/campusflow/pull/8)
contains the code and actual local test evidence.
[The PR index](docs/pull-requests.md) tracks missing review evidence.

Both fellows should contribute on separate `<type>/<actual-issue-number>-<description>`
branches and use their own identities. Each reviews the other's PR with at
least two substantive observations and final approval after fixes and testing.
Publishing this AI-authored implementation does not establish those individual
contributions or partner approvals.

See [the submission checklist](docs/submission-checklist.md) for what is
complete technically and what still requires real two-person participation.

## Limitations and possible improvements

JSON persistence is intended for one local operator: there is no locking, so
concurrent processes may overwrite changes. Tickets have no timestamps,
delete operation, authentication or audit history. Human collaboration and
learning evidence remain incomplete. Future work could add search/filtering,
backup recovery and timestamps through reviewed changes; keep the required
project standard-library-only and command-line based.
