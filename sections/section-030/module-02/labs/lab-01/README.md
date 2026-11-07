# Gate A Canary Step With An AnalysisRun

The `mission` canary must not reach 100 percent until the `probe` Service answers a check request with status 200.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
