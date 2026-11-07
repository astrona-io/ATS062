# Hold A Blue-Green Revision In Preview

The `scout` Rollout switches to a new revision as soon as it is ready. The team wants to inspect each new revision through a preview Service before any user reaches it.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
