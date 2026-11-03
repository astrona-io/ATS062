# Fundamentals Capstone: Run And Update A Rollout Behind A Service

The `bridge` service must run as a Rollout behind the existing `bridge` Service, and it must already have been updated once.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
