# Gate A Blue-Green Switch And Set The Canary Scale

Two workloads release a new revision today. `scout` may switch its active Service only after an analysis has passed. `mission` must run its canary with one pod and a traffic split through an NGINX Ingress.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
