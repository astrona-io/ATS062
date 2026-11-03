# Migrate A Deployment To A Rollout With workloadRef

The `cargo` Deployment in `starfleet` serves traffic through the `cargo` Service. The team wants Argo Rollouts to manage it without rewriting the Deployment.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
