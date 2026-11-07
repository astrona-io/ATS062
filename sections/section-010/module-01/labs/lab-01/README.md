# Create A Rollout With A Revision History Limit

The `starfleet` team wants the `mission` workload managed by Argo Rollouts instead of a Deployment.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
