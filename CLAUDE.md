# Claude behavior for this project

Do not make any file changes unless the user gives an explicit directive to do so
(e.g. "change X to Y", "add X", "delete X", "implement X", "write X").

Questions, analysis, and exploration requests ("could we...", "would it be possible...",
"does X work like Y", "verify that...", "how does...") should produce only a text answer —
no edits, no new files. When in doubt, answer first and ask before touching anything.

## Workflow
All changes must be driven by a spec under specs/original/ or specs/house-rules/.
No implementation without an approved spec. If a change is requested that lacks a spec,
write the spec first and get explicit sign-off before touching any code or config.
See specs/overview.md for the full workflow.
