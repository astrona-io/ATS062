# Complete A Canary Revision With Weight And Pause Steps

The `mission` Rollout replaces all pods at once. The team wants the new revision to take half of the pods first, wait briefly, and then take all of them.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
