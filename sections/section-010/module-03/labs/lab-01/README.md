# Configure The Controller Log Level And Format

The `argo-rollouts` controller log is hard to feed into a log collector, and a fault in the `starfleet` namespace needs more detail. Change how the controller logs.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
