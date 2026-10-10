# GitHub issues

These seven issues were created in the shared repository. Suggested role
labels have not been converted to human assignees; real usernames and team
ownership have not been supplied. The code and tests are AI-authored.

| Issue title | Suggested owner | Acceptance criteria |
| --- | --- | --- |
| [#1 Ticket creation, validation and lookup](https://github.com/miikese/campusflow/issues/1) | A | Eight fields; normalize enums; reject invalid counts including bool; no mutation/ID consumption on failure; empty lists and unknown IDs handled |
| [#2 Deterministic priority engine](https://github.com/miikese/campusflow/issues/2) | A | Exact ordered rules; four required examples; 2/3 and 9/10 boundaries; directly testable |
| [#3 Assignment and status workflow](https://github.com/miikese/campusflow/issues/3) | B | Nonblank staff; no edits to resolved; unassigned cannot progress; strict lifecycle; explicit reopen; failed operations preserve data |
| [#4 Open queue and reports](https://github.com/miikese/campusflow/issues/4) | B | Open-only queue; numeric ID tie-break; four priority ranks; empty output; all report totals match |
| [#5 Safe JSON persistence and restart](https://github.com/miikese/campusflow/issues/5) | Both | Missing-file start; strict validation; corrupted data protected; safe replacement; reload IDs unique; assignment/status round-trip |
| [#6 Automated acceptance tests and evidence](https://github.com/miikese/campusflow/issues/6) | Both | At least eight meaningful tests; all ten scenarios; temporary persistence paths; real output from latest integrated commit; independent human tests still required |
| [#7 CLI integration, documentation and genuine peer review](https://github.com/miikese/campusflow/issues/7) | Both | All menu features wired; README/run commands; real learning logs; two PRs; cross-reviews with two observations each; approval before merge; final demo |

