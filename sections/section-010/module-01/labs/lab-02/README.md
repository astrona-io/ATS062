# Set Timing Fields And Stable Metadata On A Rollout

The `starfleet` team wants a `relay` workload that waits before it counts pods as available and labels its stable pods.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
