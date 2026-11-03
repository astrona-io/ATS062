# Run An AnalysisRun With An Argument

The `starfleet` team wants to test a template by hand before it is used in a release.

Status: UNTESTED. The files were checked statically only (`astrona validate`, `bash -n`, YAML and JSON parsing). The lab has not been booted, so the grader and the reference solution have not been run against a live cluster. `testing/smoke.sh` checks that the starting state fails grading and that `solution/apply.sh` then passes.
