---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Passing Rollout Data Into An Analysis

A metric is only useful when it measures the right pods. During a canary, the query must select the canary pods, not the stable ones, and the pod names change with each revision. The `Rollout` therefore has to pass facts about the current release to the `AnalysisRun`. This part shows how arguments carry those facts and how an operator can start an `AnalysisRun` by hand.

## The analysis arguments

The `args` list of an analysis entry in a `Rollout` sets the arguments of the template. Each entry has a `name` and a `value`, or a `valueFrom`. For release data, `valueFrom` has two forms:

- `podTemplateHashValue` takes the value `Latest` or `Stable`. It gives the pod template hash of the newest ReplicaSet or of the stable ReplicaSet.
- `fieldRef.fieldPath` reads a field of the `Rollout`, for example `metadata.labels['app']`.

A template can use the hash in a query that selects pods by the label `rollouts-pod-template-hash`, so it measures exactly the canary pods.

<!-- astrona:playground:renew -->

Save this as `rollout-analysis-args.yaml`:

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
          value: "200"
      steps:
      - setWeight: 50
      - pause: {duration: 30s}
```

The template `probe-gate` takes an argument `status`. The `Rollout` sets it to `"200"`, and the value overrides the default of the template. A template that needs the pod hash would declare an argument such as `canary-hash`, and the `Rollout` would set it with `valueFrom.podTemplateHashValue: Latest`.

Apply it:

```sh
kubectl apply -f rollout-analysis-args.yaml
```

Then check the result. The command lists the `AnalysisRun` objects that the `Rollout` created:

```sh
kubectl -n starfleet get analysisruns
```

## Where an AnalysisRun comes from

The controller creates an `AnalysisRun` for each analysis entry that starts, sets the `Rollout` as its owner and copies the metrics and the resolved arguments into it. When the `Rollout` is deleted, the owned runs go with it. The controller also keeps a limited number of finished runs, set by `spec.analysis.successfulRunHistoryLimit` and `spec.analysis.unsuccessfulRunHistoryLimit`.

## Creating a run by hand

An operator can also create an `AnalysisRun` with `kubectl`, with a `spec` that has `metrics` and `args`. The run executes the same way, with no `Rollout`. This is useful to test a metric before it is used in a release. The field `spec.terminate: true` stops a running `AnalysisRun`; the run ends with the result it has so far.

Save this as `analysisrun-hand-run.yaml`. Its argument `service` names the Service that the Job requests, and the metric reads it with `{{ args.service }}`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisRun
metadata:
  name: hand-run
  namespace: starfleet
spec:
  args:
  - name: service
    value: probe
  metrics:
  - name: probe-up
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
                - import urllib.request; urllib.request.urlopen("http://{{ args.service }}:8080/", timeout=4)
```

A hand-made run has no `Rollout` and no template to supply a value, so every argument that a metric uses must have a `value` in the run itself. The controller replaces `{{ args.service }}` with `probe` before it creates the Job.

Apply it:

```sh
kubectl apply -f analysisrun-hand-run.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/hand-run --timeout=180s
kubectl -n starfleet get analysisrun hand-run -o jsonpath='{.spec.args} {.metadata.ownerReferences}{"\n"}'
```

The run ends `Successful`. The first value shows the argument as it was set, and the second is empty, because no `Rollout` owns a run that an operator created.

```mermaid
flowchart TB
  R["Rollout"] -->|"args"| A["AnalysisRun"]
  T["AnalysisTemplate"] -->|"metrics"| A
  A -->|"result"| R
```

The diagram shows that the `Rollout` and the template feed the run, and the run returns its result to the `Rollout`.

## What you know now

Arguments connect a release to its measurement, either as a plain value, a field of the `Rollout` or the hash of a ReplicaSet. The `Rollout` creates and owns the runs, and an operator can run one alone. The next question is how to read a run that did not end well.

## Common pitfalls

> [!WARNING]
> An argument that has no default and is not set by the `Rollout` makes the run end in `Error`. A query that does not select by revision measures the stable pods too, and a bad canary may then pass.
