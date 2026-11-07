# Measure A Canary With A Web Provider

The `mission` canary must not reach 100 percent until the controller itself reads status 200 from the `probe` Service.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
