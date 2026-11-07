# Run A Job-Based Analysis With An Argument

Before the next release the `starfleet` team wants a reusable health check for the `probe` Service, written as a template that takes the Service name as an argument, and proof that the check passes now.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
