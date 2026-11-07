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

## The template the examples use

Every run below comes from one `AnalysisTemplate`. It takes an argument `status` with the default `"200"`, and its single metric runs a Job that requests `/work?status=<status>` from the `probe` Service. The `probe` Service answers with the HTTP status that the request names, so `200` makes the Job succeed and `500` makes it fail.

Save this as `analysistemplate-probe-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-gate
  namespace: starfleet
spec:
  args:
  - name: status
    value: "200"
  metrics:
  - name: probe-ok
    count: 1
    failureLimit: 0
    provider:
      job:
        spec:
          backoffLimit: 0
          template:
            spec:
              restartPolicy: Never
              containers:
              - name: check
                image: docker.io/library/python:3.13-alpine
                command:
                - python
                - -c
                args:
                - import urllib.request; urllib.request.urlopen("http://probe:8080/work?status={{ args.status }}", timeout=4)
```

<!-- astrona:playground:renew -->

Apply it:

```sh
kubectl apply -f analysistemplate-probe-gate.yaml
```

## Place one: an inline analysis step

An `analysis` step in the canary steps blocks the release until the run finishes. The step names the templates and may pass arguments. The playground `Rollout` `mission` is healthy with revision `one`. Save this as `rollout-mission.yaml`. It sets the revision to `two` and puts an analysis step between the two weights:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mission
  template:
    metadata:
      labels:
        app: mission
    spec:
      containers:
      - name: mission
        image: docker.io/library/python:3.13-alpine
        env:
        - name: REVISION
          value: two
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary:
      steps:
      - setWeight: 50
      - analysis:
          templates:
          - templateName: probe-gate
          args:
          - name: status
            value: "200"
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the result. The controller creates a run when it reaches the step. It waits while the run is `Running`. A `Successful` run moves the release to the next step. A `Failed` or `Error` run aborts the release. An `Inconclusive` run pauses the release:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=300s
kubectl -n starfleet get analysisrun -o jsonpath='{range .items[*]}{.metadata.name} {.status.phase}{"\n"}{end}'
```

The list shows one run owned by `mission`, ending `Successful`, and the release reached 100 percent after it.

## Place two: a background analysis

A background analysis lives under `strategy.canary.analysis` and runs beside the steps. The field `startingStep` is the index of the step at which the run starts. Without it, the run starts with the first step. The run keeps measuring while the steps continue, so a metric with an `interval` and no `count` checks the release for its whole length. A failure at any time aborts the release.

Save this as `rollout-mission-background.yaml`. It is the same `Rollout` with revision `three`, a background analysis that asks for status `500`, and a timed pause instead of the inline step:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mission
  template:
    metadata:
      labels:
        app: mission
    spec:
      containers:
      - name: mission
        image: docker.io/library/python:3.13-alpine
        env:
        - name: REVISION
          value: three
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary:
      analysis:
        templates:
        - templateName: probe-gate
        startingStep: 1
        args:
        - name: status
          value: "500"
      steps:
      - setWeight: 50
      - pause: {duration: 60s}
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission-background.yaml
```

Then check the result. The run starts with the pause step, its Job gets an HTTP 500 error and fails, and the controller aborts the release:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.abort}'=true rollout/mission --timeout=300s
kubectl -n starfleet get analysisrun -o jsonpath='{range .items[*]}{.metadata.name} {.status.phase}{"\n"}{end}'
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.abort}{"\n"}'
```

The list now has a second run, ending `Failed`. The phase of the `Rollout` is `Degraded`, `status.abort` is `true`, and the stable ReplicaSet stays on revision `two`.

## Place three: blue-green analysis

A blue-green Rollout uses `prePromotionAnalysis` and `postPromotionAnalysis`. The pre run starts when the new pods are ready on the preview Service. The controller waits for a `Successful` run before promotion. The post run starts after the active Service moves. A `Failed` post run makes the controller switch the active Service back to the previous ReplicaSet.

## Combining the places

The three places are not exclusive. A canary can use a background analysis for a health metric over the whole release and an inline step at 50 percent for a heavier test. Each creates its own run. The controller watches all of them, and a failure in any one aborts the release. A canary can also list several templates in one step. The controller then creates one run that holds the metrics of all the templates, and the run is successful only when all of its metrics are.

Arguments follow the same order in every place. The value in the Rollout overrides the default in the template. An argument can take the hash of the pod template through `valueFrom.podTemplateHashValue` with the values `Latest` or `Stable`, which lets a metric query select the pods of one version by label.

## Common pitfalls

> [!WARNING]
> An analysis step with no matching template name in the same namespace gives an error before any measurement. A background run without a `count` runs until the release ends, so a metric with no `interval` takes only one measurement. A `ClusterAnalysisTemplate` is referenced with `clusterScope: true` on the template entry.
