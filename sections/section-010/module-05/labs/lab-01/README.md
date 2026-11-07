# Send A Rollout Notification To A Webhook

The team wants a message every time the `mission` Rollout becomes healthy. The `probe` Service in `starfleet` stores every JSON body that it receives at `/hooks`.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
