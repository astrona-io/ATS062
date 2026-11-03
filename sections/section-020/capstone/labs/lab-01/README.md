# Strategies Capstone: Preview A Blue-Green Release And Complete A Canary

Two workloads release a new revision today. `scout` must wait in preview for review. `mission` must move through canary steps by itself.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
