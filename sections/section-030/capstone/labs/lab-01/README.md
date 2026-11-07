# Block A Bad Release With Background Analysis

The release review needs proof that a failing check stops a canary. Revision two of `mission` is checked against a request that the `probe` Service answers with status 500.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
