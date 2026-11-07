# Gate A Blue-Green Switch And Set The Canary Scale

Two workloads release a new revision today. `scout` may switch its active Service only after an analysis has passed. `mission` must run its canary with one pod and a traffic split through an NGINX Ingress.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
