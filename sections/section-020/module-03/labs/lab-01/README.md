# Route A Canary Through An NGINX Ingress

External requests for `mission` enter through the Ingress `mission-ingress`. The canary must receive 20 percent of them, and requests with the header `X-Canary` must reach it.

Status: TESTED on 2026-11-07. `astrona test` booted the lab on kind (podman), ran `solution/apply.sh` and the grader passed. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) also pass. `testing/smoke.sh` checks that the starting state fails grading and that the solution then passes.
