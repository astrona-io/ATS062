# Complete A Canary Revision With Weight And Pause Steps

The `mission` Rollout replaces all pods at once. The team wants the new revision to take half of the pods first, wait briefly, and then take all of them.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
