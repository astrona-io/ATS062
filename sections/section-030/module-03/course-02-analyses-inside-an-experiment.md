---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Analyses Inside An Experiment

An experiment without a measurement only proves that pods start. The `analyses` list attaches `AnalysisTemplate` objects to the experiment, so the controller creates `AnalysisRun` objects that measure the experiment pods. This part shows how an analysis ends an experiment and how the two share their result.

## Attaching an analysis

Each entry in `spec.analyses` has a `name` and a `templateName`. It may also pass `args` and set `requiredForCompletion`. The controller creates one `AnalysisRun` for each entry when the template pods are available.

Save this as `experiment-compare.yaml`. The template `probe-gate` requests the `probe` Service with the status in its `status` argument:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Experiment
metadata:
  name: compare
  namespace: starfleet
spec:
  duration: 1m
  templates:
  - name: baseline
    replicas: 1
    selector:
      matchLabels:
        app: compare-baseline
    template:
      metadata:
        labels:
          app: compare-baseline
      spec:
        containers:
        - name: baseline
          image: docker.io/library/python:3.13-alpine
          command:
          - python
          - -m
          - http.server
          - '8080'
  - name: candidate
    replicas: 1
    selector:
      matchLabels:
        app: compare-candidate
    template:
      metadata:
        labels:
          app: compare-candidate
      spec:
        containers:
        - name: candidate
          image: docker.io/library/python:3.13-alpine
          command:
          - python
          - -m
          - http.server
          - '8080'
  analyses:
  - name: probe-check
    templateName: probe-gate
    requiredForCompletion: true
    args:
    - name: status
      value: "200"
```

<!-- astrona:playground:renew -->

Apply it:

```sh
kubectl apply -f experiment-compare.yaml
```

Then check the result. Run the commands again until the experiment is final:

```sh
kubectl -n starfleet get experiment compare
kubectl -n starfleet get analysisruns
```

## How the analysis and the duration interact

Without `requiredForCompletion`, the analyses run during the duration, and the experiment ends when the duration passes. With `requiredForCompletion: true`, the experiment does not end before that analysis ends, even after the duration. This fits an analysis that has its own `count`, which can take longer than the duration.

A `Failed` analysis fails the whole experiment at once, and the controller scales the template ReplicaSets down. An `Inconclusive` analysis makes the experiment `Inconclusive`. An `Error` analysis makes it `Error`.

## Where the AnalysisRuns come from

The `AnalysisRun` objects have the experiment as their owner. They carry the arguments of the entry, and a template that needs the address of the experiment pods can read it through a Service. This is how the analysis measures the experiment pods and not the production pods.

## What you know now

The `analyses` list creates `AnalysisRun` objects for the experiment. `requiredForCompletion` makes the experiment wait for one run, and a failed run fails the experiment. The next question is how a canary uses an experiment.

## Common pitfalls

> [!WARNING]
> A template that measures the production Service instead of the experiment pods tests nothing about the new version. A duration shorter than the time an analysis needs ends the experiment early unless `requiredForCompletion` is set.
