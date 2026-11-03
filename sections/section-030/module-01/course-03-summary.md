---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Summary

An `AnalysisTemplate` is a reusable description of what to measure. A `ClusterAnalysisTemplate` is the same without a namespace. An `AnalysisRun` is one execution: it copies the metrics, takes the measurements and holds the result. The Rollout controller creates runs from templates, and you can create a run by hand.

A template has arguments, written as `{{ args.name }}`, with a default or a required value. Each metric has a provider and the fields `count`, `interval`, `initialDelay`, `failureLimit`, `inconclusiveLimit` and `consecutiveErrorLimit`. The defaults for the limits are 0, 0 and 4. No `count` with an `interval` means the metric runs until stopped.

`successCondition` and `failureCondition` read the value `result`. With only one of them set, a measurement is good or failed. With both set, a measurement that meets neither is inconclusive. The `job` provider ignores conditions and uses the Job outcome. The `web` provider calls from the controller and needs JSON. The `prometheus` provider returns a vector read as `result[0]`.

Key facts:

- The run phases are `Pending`, `Running`, `Successful`, `Failed`, `Error` and `Inconclusive`.
- A failed metric fails the run.
- Missing arguments and empty query results give `Error`.

<!-- astrona:playground:destroy -->
