# Set Timing Fields And Stable Metadata On A Rollout

The `starfleet` team wants a `relay` workload that waits before it counts pods as available and labels its stable pods.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
