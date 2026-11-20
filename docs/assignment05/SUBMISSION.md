# Software Engineering Assignment 05 - Expense Tracker

Prepared 2026-11-20. Synthetic examples only; no real expense records or credentials were used.

## Baseline and repository map

- Repository: https://github.com/nursultanO6/expense-tracker
- Baseline commit: 9ff1eb083ec89b2a3efdc7d9463e9d326e10a1a9 (9ff1eb0 small project); working tree was clean before assignment changes.
- The baseline commit is preserved. Final source is the current working tree.
- Runtime: Python 3.9+ per README; standard library. Development dependency: pytest, unpinned in requirements.txt.
- Entry point: python -m expense_tracker -> expense_tracker/__main__.py -> cli.py.
- Modules: models.py (Expense/categories), calculator.py (validation/calculations), storage.py (JSON), reports.py (text/CSV/JSON), cli.py (argparse/dispatch).
- Tests: tests/test_calculator.py, tests/test_reports.py, tests/test_storage.py; focused standard-library checks in tests/verify_assignment05.py.
- No build scripts/configuration are present; a pure-Python CLI has no build step.

### Acceptance criteria

1. Valid positive expenses in documented categories can be added with incrementing IDs.
2. Non-positive amounts, unsupported categories, and invalid/noncanonical dates are rejected.
3. Category/month filters and totals remain correct.
4. CSV preserves descriptions with commas, quotes, and newlines; JSON reports remain valid.
5. CLI help and local JSON persistence remain supported.

### Baseline commands and results

| Command | Result |
|---|---|
| git status --short | Clean before edits. |
| git rev-parse HEAD | 9ff1eb083ec89b2a3efdc7d9463e9d326e10a1a9 |
| python --version | Python 3.14.3 |
| python -m expense_tracker --help | Passed; usage and subcommands printed. |
| python -m pytest -q on baseline commit 9ff1eb0, cloned fresh from GitHub | PASS: 14 passed in 0.03s. The clone was clean at the baseline hash. |
| Lint/type/build | No configured lint, type-check, or build commands. Not run. |

Source evidence at baseline: reports.py interpolated CSV fields into raw comma-separated lines; calculator.py stored date_str without calendar validation. Baseline tests were run against a fresh clone of commit 9ff1eb0.

## Agent instructions

Root AGENTS.md documents purpose, architecture, setup, safe commands, coding conventions, acceptance criteria, forbidden actions, and human review gates. Codex read it explicitly; this task did not rely on automatic discovery. Boundaries prohibit handling secrets or real records, production actions, destructive commands, unreviewed dependency changes, and unapproved commit/merge/publishing.

## Pattern decision

The renderer has a small format conditional for three related formats. Strategy was evaluated, but extra report classes would add indirection without reducing meaningful coupling. No pattern was warranted. The focused structural change uses Python's standard csv.writer in the current CSV branch. Before, fields were concatenated into strings; after, CSV escaping is handled by the standard library and dispatch remains local.

## Risk register

Findings were checked against source and commands. Confirmed means source behavior is demonstrable, not that a production incident occurred. Score = likelihood x impact, each 1-3. The two highest-ranked confirmed findings were mitigated.

| ID | Category/status | Cause -> event -> consequence; evidence | LxI=score | Mitigation, owner, verification | Residual risk |
|---|---|---|---:|---|---|
| R1 | Correctness, confirmed | reports.py originally interpolated descriptions directly into CSV; delimiters/quotes/newlines could corrupt fields for consumers. Original source used a formatted string with commas. Final regression round-trips special characters. | 3x2=6 | csv.writer plus regression coverage. Owner: maintainer. Verified by the focused check and the full pytest run (16 passed). | Consumers may expect another delimiter/encoding; output is comma-delimited without a BOM. |
| R2 | Correctness, confirmed | calculator.add_expense stored date_str as-is; invalid dates could pollute records and make filters/reports misleading. Baseline had no validation; focused checks reject impossible/noncanonical values. | 2x2=4 | Parse with date.fromisoformat and require canonical round-trip; regression coverage. Owner: maintainer. Verified by the focused checks and the full pytest run (16 passed). | Legacy JSON records are not migrated or validated on load. |
| R3 | Correctness, plausible/unverified | storage.save_expenses opens the destination in write mode; interruption during write could leave truncated JSON. Direct overwrite is visible in source; interruption damage was not reproduced. | 2x3=6 | Consider temp file + atomic replace after failure-injection testing. Owner: maintainer. Verify using disposable data. | No atomic-write safeguard added; this remains plausible, not confirmed. |
| R4 | Dependency, confirmed fact/plausible impact | requirements.txt contains unpinned pytest; clean environments may resolve different versions over time. No break was observed. | 2x2=4 | Choose a supported pin/lock after checking Python compatibility. Owner: maintainer. Verify in clean environment. | Reproducibility remains partial: pytest installed and ran locally, but no version is pinned. No dependency change made. |
| R5 | Security, unsupported as vulnerability; confirmed interface | --file accepts a caller-selected path and save_expenses overwrites it. An operator could choose an unintended file; normal use is local and user-directed, with no remote input or privilege boundary. No exploit or unintended overwrite demonstrated. | 1x3=3 | Use disposable paths for write tests and review file arguments. Owner: operator. Verify test commands. | User path mistakes remain possible; evidence does not support calling this an exploitable flaw. |
| R6 | Agent operations, confirmed | No CI, lint/type configuration, or build script exists; an agent cannot rely on those automation gates. Repository inventory confirms absence. | 2x2=4 | Keep safe commands/review gates in AGENTS.md; add CI only when warranted. Owner: maintainer. Verify repository inventory. | Human review remains necessary; no CI evidence exists. |

Top confirmed corrective actions: R1 (6) and R2 (4). R3 also scores 6 but is plausible/unverified, so it is not represented as a confirmed defect or completed mitigation.

## Agent-readiness audit

| Area | Evidence |
|---|---|
| Readable structure | Five focused modules and tests; boundaries are clear. |
| README | Documents setup, commands, categories; updated for date/CSV behavior and focused checks. |
| Reproducibility | Runtime uses standard library; requirements.txt does not pin pytest, so fresh test environments may resolve different versions. The user PowerShell run confirms the current suite passes. Partial. |
| Tests | Baseline: 14 passed. Final: 16 passed in the user's PowerShell environment without an adapter. |
| Lint/type/build | No configured tools/build step. |
| Logging | CLI prints validation/format errors; no logging framework, reasonable for a small CLI. |
| Security | No credentials or external services; local path is user-selected. Boundaries are in AGENTS.md. |
| Instructions | AGENTS.md includes architecture, safe commands, forbidden actions, criteria, and review gates. |

Readiness level: 2 - Documented. Level 3 is not supported because dependencies are not pinned and CI/lint/type/build gates are absent. Missing evidence: pinned dependency, CI verification, lint/type checks.

## Mitigations and final verification

1. R1: replaced manual CSV concatenation with csv.writer; added pytest regression for commas, quotes, and newlines. No dependency added.
2. R2: validate provided dates as real canonical ISO dates before constructing an expense; tests cover impossible dates, non-padded dates, and arbitrary text. Default date behavior remains unchanged.

| Final command | Actual result |
|---|---|
| python -m tests.verify_assignment05 | PASS: 7 standard-library checks. |
| python -m compileall -q expense_tracker tests | PASS; no syntax errors. |
| python -m expense_tracker --help | PASS; help printed. |
| git diff --check | PASS; no whitespace errors. Git warned about line-ending normalization. |
| python -m pytest -q (PowerShell, user-run) | PASS: 16 passed in 0.13s. No tmp_path adapter was used. |

Accounting: baseline pytest 14 passed, 0 failed; final pytest 16 passed, 0 failed; 7 focused checks passed, 0 failed. The final run was the user's ordinary PowerShell run with no fixture adapter. Raw output transcripts are included as pytest-baseline.txt and pytest-final.txt. No screenshots: this is a text CLI with no visual interface.

Residual risks: R1/R2 are covered by regression tests and the full suite passes. R3/R4/R5/R6 remain as classified above.

## Hypothetical asynchronous-agent safeguards

- Use an isolated branch/worktree from the reviewed baseline; do not share the human working tree.
- Allowed files: expense_tracker/calculator.py, expense_tracker/reports.py, directly related tests, and a task-specific notes file. Expansion requires review first.
- Allowed commands: syntax check, focused tests, pytest if already installed, git diff, read-only inspection. Limit: 20 minutes; stop if a check needs a new package or network.
- Prohibited: secrets/real records, destructive commands, dependency changes, deployment, push/merge/commit/publication, or edits outside the allowed list.
- Required artifacts: change summary, complete diff, test logs with exact commands, build result or not applicable, risk notes.
- Human reviews the diff and evidence and approves before merge/deployment. On failure, discard/reset only the isolated worktree/branch to its recorded starting commit, retain logs, and report why. Never roll back the user's main tree automatically.

## Release decision

CONDITIONAL. The full pytest suite passes (16 passed), the 7 standalone checks pass, syntax compilation and CLI help succeed, and R1/R2 have direct regression coverage. There is no production deployment or external service in scope. It is not GO because known limitations remain that need explicit controls: R3 (non-atomic JSON write, plausible, not reproduced), R4 (unpinned pytest) and R6 (no CI/lint/type gates). Owner: project maintainer/student. Conditions: assess R3 with a failure-injection test before relying on the JSON file for important records; pin a supported pytest version; add CI when warranted.

## AI-use record and evidence appendix

- Assistant 1: Claude (Anthropic), Claude chat app; date 2026-11-20. Prompts (summary): asked for a small, non-sensitive project suitable for this assignment, then asked it to review the completed work. Output used: the baseline starter project (expense_tracker package, tests, README). Review output used: notes that local pytest evidence was missing, that Claude must be listed in this record, and an optional note on render_summary CSV consistency (not changed). Verification: Claude reported 14 baseline and 16 final tests passing in its own sandbox; I reran the final suite locally (16 passed).
- Assistant 2: OpenAI Codex, GPT-6 (as recorded by that session); date 2026-11-20.
- Context: user-provided assignment text, repository source/tests/README, baseline commit, and actual command outputs. No real financial data or credentials.
- Risk-review task prompt used in this session: inspect the repository read-only for candidate correctness, maintainability, security, dependency, and agent-operation risks; make no changes during that review; verify each claim against source or commands.
- Output used: candidates R1-R6 in the risk register, with R1 CSV interpolation and R2 missing date validation confirmed from source. The suggested CSV writer and strict date validation became the two focused mitigations; no design pattern was added.
- Decisions: R1/R2 were fixed and regression checks added; R3 stays plausible/unverified; R5 is not labeled a vulnerability; readiness is level 2 and release is conditional because R3 is unmitigated and pytest is unpinned.
- Verification: I inspected the source and diff, ran the baseline and final suites, executed the focused checks, and recorded the outputs above. I reviewed each risk against source evidence and separated confirmed from plausible or unsupported claims.
- Codex sandbox note: Codex first used Python 3.14.3 without pytest, then located pytest 8.4.2 in Anaconda Python 3.13.9. That separate sandbox required a temporary tmp_path adapter. My PowerShell run passed all 16 tests without an adapter; the two environments are not conflated in this report.
- Changes: canonical date validation; CSV writer; pytest regression tests and standard-library checks; README; AGENTS.md; this audit.
- Verification sources: baseline Git/status, source inspection, exact commands above, and final diff review. Unverified risks are explicitly separated from confirmed findings.

### AI reflection

I used Claude (Anthropic) and OpenAI Codex while completing this assignment. Claude helped me select and create a small expense-tracker project, and it later reviewed the work. I gave Codex the assignment instructions, project source and tests, README, baseline commit, and command results. I asked it to inspect the code for risks before making changes, propose targeted mitigations, and prepare evidence for the release decision.

The most useful finding was that the CSV renderer joined fields with commas directly. I checked the code and confirmed that descriptions with commas, quotation marks, or line breaks could be misread by spreadsheet tools. I accepted the change to Python's csv.writer and checked the result by parsing a report containing those characters. I also confirmed that supplied dates were stored without validation and reviewed the new cases for impossible and noncanonical dates. My baseline pytest run passed 14 tests. I then ran python -m pytest -q in PowerShell on the final project; 16 tests passed in 0.13 seconds, with no tmp_path adapter. I also ran seven focused checks, syntax compilation, CLI help, and a whitespace check.

The tests support a CONDITIONAL release decision, but they do not address the plausible risk of a partial JSON write if the process stops during saving. The repository instructions improved the process by spelling out safe commands, boundaries, acceptance criteria, and review gates. I chose not to add a design pattern: the report-format branch is small, and Strategy classes would add indirection without fixing a demonstrated maintenance problem. My next steps would be to test atomic JSON writes and pin pytest once the supported version range is decided.
