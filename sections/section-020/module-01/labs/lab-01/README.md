# Hold A Blue-Green Revision In Preview

The `scout` Rollout switches to a new revision as soon as it is ready. The team wants to inspect each new revision through a preview Service before any user reaches it.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
