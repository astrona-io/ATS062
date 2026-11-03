# Analysis Capstone: Block A Bad Release With Background Analysis

The release review needs proof that a failing check stops a canary. Revision two of `mission` is checked against a request that the `probe` Service answers with status 500.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
