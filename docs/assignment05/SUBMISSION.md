# Software Engineering Assignment 05 вЂ” Expense Tracker

Prepared 2026-11-20. Synthetic examples only; no real expense records or credentials were used.

## Baseline and repository map

- Repository: https://github.com/nursultanO6/expense-tracker
- Baseline commit: 9ff1eb083ec89b2a3efdc7d9463e9d326e10a1a9 (9ff1eb0 small project); working tree was clean before assignment changes.
- The baseline commit is preserved. Final source is the current working tree.
- Runtime: Python 3.9+ per README; standard library. Development dependency: pytest, unpinned in requirements.txt.
- Entry point: python -m expense_tracker в†’ expense_tracker/__main__.py в†’ cli.py.
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
| python -m pytest (Anaconda Python 3.13.9) -q -p no:cacheprovider on isolated baseline snapshot | PASS: 14 passed in 0.04s. Snapshot expanded from baseline commit 9ff1eb0; a temporary workspace-backed tmp_path fixture adapter was used because the default temp folder was inaccessible in this sandbox. |
| Lint/type/build | No configured lint, type-check, or build commands. Not run. |

Source evidence at baseline: reports.py interpolated CSV fields into raw comma-separated lines; calculator.py stored date_str without calendar validation. Baseline tests were run against an isolated snapshot of commit 9ff1eb0.

## Agent instructions

Root AGENTS.md documents purpose, architecture, setup, safe commands, coding conventions, acceptance criteria, forbidden actions, and human review gates. Codex read it explicitly; this task did not rely on automatic discovery. Boundaries prohibit handling secrets or real records, production actions, destructive commands, unreviewed dependency changes, and unapproved commit/merge/publishing.

## Pattern decision

The renderer has a small format conditional for three related formats. Strategy was evaluated, but extra report classes would add indirection without reducing meaningful coupling. No pattern was warranted. The focused structural change uses Python's standard csv.writer in the current CSV branch. Before, fields were concatenated into strings; after, CSV escaping is handled by the standard library and dispatch remains local.

## Risk register

Findings were checked against source and commands. Confirmed means source behavior is demonstrable, not that a production incident occurred. Score = likelihood Г— impact, each 1вЂ“3. The two highest-ranked confirmed findings were mitigated.

| ID | Category/status | Cause в†’ event в†’ consequence; evidence | LГ—I=score | Mitigation, owner, verification | Residual risk |
|---|---|---|---:|---|---|
| R1 | Correctness, confirmed | reports.py originally interpolated descriptions directly into CSV; delimiters/quotes/newlines could corrupt fields for consumers. Original source used a formatted string with commas. Final regression round-trips special characters. | 3Г—2=6 | csv.writer plus regression coverage. Owner: maintainer. Verified by the focused check and the full pytest run (16 passed). | Consumers may expect another delimiter/encoding; output is comma-delimited without a BOM. |
| R2 | Correctness, confirmed | calculator.add_expense stored date_str as-is; invalid dates could pollute records and make filters/reports misleading. Baseline had no validation; focused checks reject impossible/noncanonical values. | 2Г—2=4 | Parse with date.fromisoformat and require canonical round-trip; regression coverage. Owner: maintainer. Verified by the focused checks and the full pytest run (16 passed). | Legacy JSON records are not migrated or validated on load. |
| R3 | Correctness, plausible/unverified | storage.save_expenses opens the destination in write mode; interruption during write could leave truncated JSON. Direct overwrite is visible in source; interruption damage was not reproduced. | 2Г—3=6 | Consider temp file + atomic replace after failure-injection testing. Owner: maintainer. Verify using disposable data. | No atomic-write safeguard added; this remains plausible, not confirmed. |
| R4 | Dependency, confirmed fact/plausible impact | requirements.txt contains unpinned pytest; clean environments may resolve different versions over time. No break was observed. | 2Г—2=4 | Choose a supported pin/lock after checking Python compatibility. Owner: maintainer. Verify in clean environment. | Reproducibility remains partial: pytest installed and ran locally, but no version is pinned. No dependency change made. |
| R5 | Security, unsupported as vulnerability; confirmed interface | --file accepts a caller-selected path and save_expenses overwrites it. An operator could choose an unintended file; normal use is local and user-directed, with no remote input or privilege boundary. No exploit or unintended overwrite demonstrated. | 1Г—3=3 | Use disposable paths for write tests and review file arguments. Owner: operator. Verify test commands. | User path mistakes remain possible; evidence does not support calling this an exploitable flaw. |
| R6 | Agent operations, confirmed | No CI, lint/type configuration, or build script exists; an agent cannot rely on those automation gates. Repository inventory confirms absence. | 2Г—2=4 | Keep safe commands/review gates in AGENTS.md; add CI only when warranted. Owner: maintainer. Verify repository inventory. | Human review remains necessary; no CI evidence exists. |

Top confirmed corrective actions: R1 (6) and R2 (4). R3 also scores 6 but is plausible/unverified, so it is not represented as a confirmed defect or completed mitigation.

## Agent-readiness audit

| Area | Evidence |
|---|---|
| Readable structure | Five focused modules and tests; boundaries are clear. |
| README | Documents setup, commands, categories; updated for date/CSV behavior and focused checks. |
| Reproducibility | Runtime uses standard library; pytest 8.4.2 was available in the existing Anaconda Python 3.13.9 install, but requirements.txt does not pin it. Partial. |
| Tests | Baseline: 14 passed. Final: 16 passed. A temporary workspace-backed tmp_path fixture adapter was used only for the sandboxed run and removed afterward. |
| Lint/type/build | No configured tools/build step. |
| Logging | CLI prints validation/format errors; no logging framework, reasonable for a small CLI. |
| Security | No credentials or external services; local path is user-selected. Boundaries are in AGENTS.md. |
| Instructions | AGENTS.md includes architecture, safe commands, forbidden actions, criteria, and review gates. |

Readiness level: 2 вЂ” Documented. Level 3 is not supported because dependencies are not pinned and CI/lint/type/build gates are absent. Missing evidence: pinned dependency, CI verification, lint/type checks.

## Mitigations and final verification

1. R1: replaced manual CSV concatenation with csv.writer; added pytest regression for commas, quotes, and newlines. No dependency added.
2. R2: validate provided dates as real canonical ISO dates before constructing an expense; tests cover impossible dates, non-padded dates, and arbitrary text. Default date behavior remains unchanged.

| Final command | Actual result |
|---|---|
| python -m tests.verify_assignment05 | PASS: 7 standard-library checks. |
| python -m compileall -q expense_tracker tests | PASS; no syntax errors. |
| python -m expense_tracker --help | PASS; help printed. |
| git diff --check | PASS; no whitespace errors. Git warned about line-ending normalization. |
| python -m pytest (Anaconda Python 3.13.9) -q -p no:cacheprovider | PASS: 16 passed in 0.10s. A temporary fixture adapter redirected tmp_path into a shell-created workspace folder; tests and application files were otherwise unchanged. |

Accounting: baseline pytest 14 passed, 0 failed; final pytest 16 passed, 0 failed; 7 focused checks passed, 0 failed. Pytest's default temporary directory was inaccessible, so a temporary workspace-backed tmp_path fixture adapter was used to run the two persistence tests; it was removed after the run. No screenshots: this is a text CLI with no visual interface.

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
- Output used: candidates R1вЂ“R6 in the risk register, with R1 CSV interpolation and R2 missing date validation confirmed from source. The suggested CSV writer and strict date validation became the two focused mitigations; no design pattern was added.
- Decisions: R1/R2 were fixed and regression checks added; R3 stays plausible/unverified; R5 is not labeled a vulnerability; readiness is level 2 and release is conditional because R3 is unmitigated and pytest is unpinned.
- Verification: I inspected the source and diff, ran the baseline and final suites, executed the focused checks, and recorded the outputs above. I reviewed each risk against source evidence and separated confirmed from plausible or unsupported claims.
- Environment issue resolved: the default Python 3.14.3 environment lacked pytest, but pytest 8.4.2 was installed in the existing Anaconda Python 3.13.9 environment. Its default temporary directory was inaccessible in this sandbox, so I temporarily redirected tmp_path into a shell-created workspace directory. Baseline and final tests then passed; the adapter was removed.
- Changes: canonical date validation; CSV writer; pytest regression tests and standard-library checks; README; AGENTS.md; this audit.
- Verification sources: baseline Git/status, source inspection, exact commands above, and final diff review. Unverified risks are explicitly separated from confirmed findings.

### AI reflection

I used Claude (Anthropic) and OpenAI Codex on November 20, 2026. Claude helped create the small expense-tracker project and later reviewed the completed work. I gave Codex the assignment, the repository source and tests, the README, the baseline commit, and command output. I asked it to identify risks before editing, make two focused improvements, and prepare evidence for the release decision. I checked the key findings against the code. The most useful suggestion was that manually joining CSV fields can corrupt descriptions with commas, quotes, or line breaks. I confirmed the renderer used string interpolation, accepted the focused csv.writer change, and verified the output by parsing it back with Python's CSV reader. I also confirmed that supplied dates were stored without validation, then checked that impossible and noncanonical dates are rejected.

I initially ran pytest with Python 3.14.3 and found that pytest was missing. I then located pytest 8.4.2 in my existing Anaconda Python 3.13.9 installation. The sandbox blocked pytest's default temporary folder, so I used a temporary workspace-backed tmp_path fixture adapter for the persistence tests and removed it afterward. The preserved baseline passed 14 tests; the final version passed 16. I also ran seven focused checks, syntax compilation, CLI help, and a whitespace check. This testing changed the release decision: the targeted changes are covered, but I kept the decision CONDITIONAL because JSON writes are not atomic and pytest is unpinned. The AGENTS.md instructions improved the process by documenting safe commands, prohibited actions, acceptance criteria, and human review gates. I did not add a design pattern because report dispatch remains small; Strategy classes would add indirection without solving a demonstrated maintenance problem. Next I would assess atomic writes and pin pytest after settling the supported versions.

