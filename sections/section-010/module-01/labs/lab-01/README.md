# Reconcile A Rollout And Its ReplicaSet

The `starfleet` team wants the `mission` workload managed by Argo Rollouts instead of a Deployment.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
