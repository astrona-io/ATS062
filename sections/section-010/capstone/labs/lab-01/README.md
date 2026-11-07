# Run And Update A Rollout Behind A Service

The `bridge` service must run as a Rollout behind the existing `bridge` Service, and it must already have been updated once.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
