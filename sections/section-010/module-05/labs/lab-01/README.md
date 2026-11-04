# Send A Rollout Notification To A Webhook

The team wants a message every time the `mission` Rollout becomes healthy. The `probe` Service in `starfleet` stores every JSON body that it receives at `/hooks`.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
