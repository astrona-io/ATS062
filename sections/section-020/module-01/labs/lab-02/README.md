# Run A Blue-Green Rollout With A Small Preview

The `starfleet` team wants a blue-green `relay` workload with active and preview Services and role labels on the active pods.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
