# Run A Job-Based Analysis With An Argument

Before the next release the `starfleet` team wants a reusable health check for the `probe` Service, written as a template that takes the Service name as an argument, and proof that the check passes now.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
