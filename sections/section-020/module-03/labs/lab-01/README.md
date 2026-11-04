# Route A Canary Through An NGINX Ingress

External requests for `mission` enter through the Ingress `mission-ingress`. The canary must receive 20 percent of them, and requests with the header `X-Canary` must reach it.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
