---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Summary

An `AnalysisRun` moves from `Pending` to `Running` and ends in `Successful`, `Failed`, `Error` or `Inconclusive`. It keeps a copy of its arguments and metrics from the time it was created, and the Rollout owns the runs it creates. The controller terminates a run when the release is aborted or replaced.

A Rollout runs analysis in three ways. An inline `analysis` step blocks the canary at that step. A background analysis under `strategy.canary.analysis` runs beside the steps from `startingStep`. A blue-green Rollout runs `prePromotionAnalysis` before the switch and `postPromotionAnalysis` after it, and a failed post run returns the active Service to the old version.

A `Successful` run continues the release. A `Failed` or `Error` run aborts it and sets `status.abort`. An `Inconclusive` run pauses it for a person. The reason is in `status.metricResults`, the measurements, and for a `job` provider the Job logs. An `Experiment` runs temporary ReplicaSets, such as the stable and the canary specs, and analyses them for a set duration.

The `Rollout` passes release data into the analysis through arguments, including the hash of the latest or the stable ReplicaSet, and it owns the `AnalysisRun` objects it creates. An operator can also create a run by hand and stop it with `terminate`. To find the cause of an abort, read the message of the `Rollout`, then the run, then the metric result and then the measurement.

Key facts:

- An abort returns the weight to 0 and the phase becomes `Degraded`.
- `consecutiveErrorLimit` protects against short outages of a metric server.
- A `ClusterAnalysisTemplate` needs `clusterScope: true` in the reference.
- A run is `Failed`, `Error` or `Inconclusive` depending on its metrics.
- `Error` means the measurement itself broke.

<!-- astrona:playground:destroy -->
