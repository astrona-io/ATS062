# Gate A Canary Step With An AnalysisRun

The `mission` canary must not reach 100 percent until the `probe` Service answers a check request with status 200.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
