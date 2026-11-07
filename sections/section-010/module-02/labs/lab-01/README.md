# Migrate A Deployment To A Rollout With workloadRef

The `cargo` Deployment in `starfleet` serves traffic through the `cargo` Service. The team wants Argo Rollouts to manage it without rewriting the Deployment.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
