# How to test CampusFlow yourself

Use a terminal at the project root. Python 3.10+ is required; no pip installs.
On Windows replace `python3` with `py -3` if needed.

## 1. Run all automated tests

```sh
python3 -m unittest discover -s tests -v
```

Expected: **49 tests and OK**. Each `... ok` means that test's assertions
passed. `FAIL` means a wrong result; `ERROR` means an exception or setup issue.
Read the traceback, fix the cause and rerun the affected group before the full
suite. Do not delete an assertion merely to hide a bug.

Tests use temporary directories and do not touch your saved helpdesk tickets.
The checked-in `test-output.txt` is actual execution evidence from this session;
run the command yourself for evidence of your own verification.

## 2. Test the two feature groups separately

Engineer A — creation, validation, priority and IDs:

```sh
python3 -m unittest tests.test_tickets -v
```

Engineer B — assignment, lifecycle, reopening, queue and reports:

```sh
python3 -m unittest tests.test_workflow -v
```

Shared — JSON loading/saving and full interactive flows:

```sh
python3 -m unittest tests.test_storage -v
python3 -m unittest tests.test_cli -v
```

For one specific test:

```sh
python3 -m unittest tests.test_tickets.PriorityTests.test_all_rule_boundaries -v
python3 -m unittest tests.test_workflow.WorkflowTests.test_unassigned_ticket_cannot_start_and_state_is_preserved -v
```

## 3. What the tests verify

| Area | Cases you should check | Expected behavior |
| --- | --- | --- |
| Priority | high/12, high/2, low/4, low/1 | critical, high, medium, low |
| Boundaries | high/9 vs high/10; low/2 vs low/3; low/9 vs low/10; medium/1 | high vs critical; low vs medium; medium vs high; medium |
| Creation | blank/whitespace title, invalid category/urgency | Useful error, unchanged list and next ID |
| Counts | 0, -1, 1.5, text, True, False | Rejected; positive integers accepted |
| Normalization | nEtWoRk, HIGH, t001, extra spaces | Canonical values; trimmed title/staff |
| Details | empty list, T999, valid ID | Clear empty/error feedback; all eight fields for valid ticket |
| Assignment | blank staff, unknown ID, resolved record | Rejected without changing the ticket |
| Lifecycle | unassigned → in_progress; assigned open → in_progress → resolved | First rejected; assigned lifecycle accepted |
| Invalid transitions | open → resolved, in_progress → open, same status | Rejected without mutation |
| Reopening | resolved ticket vs open/in_progress ticket | Resolved becomes open retaining staff; others rejected |
| Queue | all priorities, T002/T010/T1000, other statuses | Priority then numeric ID; only open tickets |
| Reports | empty and mixed records | All eight counts; each breakdown sums to total |
| Persistence | save/reload, assigned/resolved records, gaps and T999 | All fields preserved; next ID T1000 after T999 |
| Bad data | invalid JSON/UTF-8/schema, duplicate IDs/keys, wrong priority | Error; original file unchanged |
| Save failure | simulated replacement failure | Original file preserved and temporary file removed |
| CLI | invalid menu input, exit, EOF/Ctrl+C, real restart | No ordinary-input crash; completed pending changes saved |

## 4. Run the repeatable demo

```sh
python3 main.py --demo
```

It creates four different priorities, checks boundaries, rejects zero users
and unassigned progress, assigns/resolves a ticket, shows queue/report counts,
checks T002 before T010 before T1000, reloads JSON and creates T005.
Expected final line: `Demo assertions passed. Run unittest separately for automated test evidence.`
The demo uses temporary storage and leaves your saved tickets alone.

## 5. Perform your own interactive check

Start with a separate practice file that does not already exist:

```sh
python3 main.py --data data/manual-check.json
```

If you used that file before, close the app and move it to a backup first.
With fresh data, option 2 shows no tickets, option 7 shows no open tickets,
and option 8 shows all zeros.

Choose option 1 four times and enter:

| ID expected | Title | Category | Urgency | Users | Priority expected |
| --- | --- | --- | --- | --- | --- |
| T001 | Campus Wi-Fi down | Network | high | 12 | critical |
| T002 | Broken laptop | Hardware | high | 2 | high |
| T003 | Development tools | Software | low | 4 | medium |
| T004 | General question | Other | low | 1 | low |

Then check these steps in order:

1. Option 1: try title `Invalid count`, category `Other`, urgency `low`, users `0`.
   Expect rejection. Option 2 must still show exactly four tickets.
2. Option 3 with `T001`: verify all eight fields, open status and unassigned staff.
3. Option 5 with `T002` and `in_progress`: expect rejection. View it again;
   status must still be open.
4. Option 7: expected queue T001, T002, T003, T004.
5. Option 8: total 4; open 4, in_progress 0, resolved 0; each priority count 1.
6. Option 4 with `T001` and `Demo Staff`, then option 5 with `T001` and `in_progress`.
   Option 7 must now exclude T001, even though it is critical.
7. Option 5 with `T001` and `resolved`. View details: resolved and Demo Staff.
   Report: total 4; open 3, in_progress 0, resolved 1; each priority still 1.
8. Try option 4 to reassign T001 and option 5 to set T001 to open. Both must
   fail, leaving staff/status unchanged.
9. Option 6 with T001: expected open status, retaining Demo Staff.
10. Option 9 saves; option 0 exits. Restart with the **same --data command**.
    Option 2 must show four tickets, including T001's assignment.
11. Create one more valid ticket. Expect T005, proving rejected creation and
    restart did not consume or duplicate an ID.

## 6. Verify damaged-data protection

Use a separate file, never your real saved tickets:

```sh
python3 -c "from pathlib import Path; Path('data').mkdir(exist_ok=True); Path('data/broken-check.json').write_text('{broken', encoding='utf-8')"
python3 main.py --data data/broken-check.json
python3 -c "from pathlib import Path; print(Path('data/broken-check.json').read_text(encoding='utf-8'))"
```

Expect startup to stop with a clear error and exit status 1. The last command
must still print `{broken`; it must not become `[]` or disappear.

## 7. Keep truthful evidence

Record the command you personally ran, actual output, Git commit tested and
your explanation of the result. Distinguish AI-authored code from your own
contribution. The technical suite cannot demonstrate real partner learning,
reviews or approvals; those require genuine people and GitHub evidence.
