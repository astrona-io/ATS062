---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Summary

An `Experiment` runs temporary ReplicaSets for a set time. Each entry in `spec.templates` has a name, a replica count, a selector and a pod template. The `duration` sets the length, and without it the experiment ends when its analyses end. A final phase is `Successful`, `Failed`, `Error` or `Inconclusive`.

The `analyses` list creates an `AnalysisRun` for each entry. A `Failed` run fails the experiment at once, and `requiredForCompletion` makes the experiment wait for a run even after the duration. The runs are owned by the experiment.

A canary step named `experiment` creates an owned `Experiment`. Its templates use `specRef` to copy the pod spec of the stable or the canary ReplicaSet. A successful experiment moves the release on, a failed one aborts it and an inconclusive one pauses it. With a traffic router, a template can receive a weight.

The status lists `templateStatuses` and `analysisRuns`. Events and the owned runs give the cause of a failure. Pods are scaled down at the end, so read logs during the run.

Key facts:

- The selector must match the template labels.
- `specRef` accepts `stable` and `canary`.
- A `Failed` analysis fails the experiment.
- The experiment object stays after the end.

<!-- astrona:playground:destroy -->
