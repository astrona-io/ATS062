---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# The AnalysisRun Lifecycle And Where A Rollout Runs It

The controller creates an `AnalysisRun` when a release reaches the point where analysis is configured. This part follows one run from creation to its final phase and shows the three places in a Rollout where analysis can be placed.

## The lifecycle of a run

An `AnalysisRun` goes through these phases:

1. `Pending`: the run exists and the controller has not started it.
2. `Running`: the controller takes measurements. The results are stored in `status.metricResults`, one entry per metric, each with its own list of measurements.
3. A final phase: `Successful`, `Failed`, `Error` or `Inconclusive`.

A run is terminal when it reaches a final phase. The controller does not change it afterwards. A run that the Rollout created has an owner reference to the Rollout, so deleting the Rollout deletes its runs. Each run keeps the arguments and metrics as they were at creation. Editing the template later does not change a run that exists.

A run can also be stopped from outside. When the release is aborted or replaced by a newer revision, the controller sets `spec.terminate: true` on the run. The run then ends early, and the controller treats a run that was terminated by the controller as successful, because the stop was not caused by a bad measurement.

## Place one: an inline analysis step

An `analysis` step in the canary steps blocks the release until the run finishes. The step names the templates and may pass arguments:

```yaml
strategy:
  canary:
    steps:
    - setWeight: 20
    - analysis:
        templates:
        - templateName: probe-gate
        args:
        - name: status
          value: "200"
    - setWeight: 100
```

The controller creates a run when it reaches the step. It waits while the run is `Running`. A `Successful` run moves the release to the next step. A `Failed` or `Error` run aborts the release. An `Inconclusive` run pauses the release.

## Place two: a background analysis

A background analysis lives under `strategy.canary.analysis` and runs beside the steps:

```yaml
strategy:
  canary:
    analysis:
      templates:
      - templateName: probe-gate
      startingStep: 1
      args:
      - name: status
        value: "200"
    steps:
    - setWeight: 20
    - pause: {duration: 60s}
    - setWeight: 100
```

The field `startingStep` is the index of the step at which the run starts. Without it, the run starts with the first step. The run keeps measuring while the steps continue, so a metric with an `interval` and no `count` checks the release for its whole length. A failure at any time aborts the release.

## Place three: blue-green analysis

A blue-green Rollout uses `prePromotionAnalysis` and `postPromotionAnalysis`. The pre run starts when the new pods are ready on the preview Service. The controller waits for a `Successful` run before promotion. The post run starts after the active Service moves. A `Failed` post run makes the controller switch the active Service back to the previous ReplicaSet.

<!-- astrona:playground:renew -->

## Adding a background analysis

In the playground, the Rollout `mission` is healthy with revision `one`. Save a copy of its manifest, add a `strategy.canary.analysis` block that uses a template named `probe-gate` with the argument `status` set to `"500"`, and add two steps `setWeight: 50` and `pause: {duration: 60s}`. Apply the Rollout, then change the `REVISION` environment variable to `two` and apply it again.

The `probe` Service answers a request for status 500 with an HTTP 500 error. The template's Job fails, and the background run ends in the `Failed` phase. Read the objects the controller created:

```sh
kubectl -n starfleet get analysisrun
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.abort}{"\n"}'
```

The Rollout is aborted and the stable ReplicaSet stays on revision `one`.

## Combining the places

The three places are not exclusive. A canary can use a background analysis for a health metric over the whole release and an inline step at 50 percent for a heavier test. Each creates its own run. The controller watches all of them, and a failure in any one aborts the release. A canary can also list several templates in one step. The controller then creates one run that holds the metrics of all the templates, and the run is successful only when all of its metrics are.

Arguments follow the same order in every place. The value in the Rollout overrides the default in the template. An argument can take the hash of the pod template through `valueFrom.podTemplateHashValue` with the values `Latest` or `Stable`, which lets a metric query select the pods of one version by label.

## Common pitfalls

> [!WARNING]
> An analysis step with no matching template name in the same namespace gives an error before any measurement. A background run without a `count` runs until the release ends, so a metric with no `interval` takes only one measurement. A `ClusterAnalysisTemplate` is referenced with `clusterScope: true` on the template entry.
