---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# The Template, Its Arguments And Its Metrics

An `AnalysisTemplate` is a Kubernetes object that describes what to measure and what result counts as good. It does not run anything by itself. A separate object, the `AnalysisRun`, runs the measurements. This part explains the template and the fields that control its metrics.

## Three related resources

- An `AnalysisTemplate` is namespaced. A Rollout can use it only in the same namespace.
- A `ClusterAnalysisTemplate` has the same fields but no namespace. A Rollout in any namespace can use it.
- An `AnalysisRun` is one execution. It holds a copy of the metrics at the time it was created, plus the measurements and the result. It is a namespaced object.

The Rollout controller creates an `AnalysisRun` from a template when a release reaches an analysis step. You can also create an `AnalysisRun` yourself, for a one-off check, with the same `spec` fields as a template.

## Arguments

A template can declare arguments in `spec.args`. An argument has a `name` and either a `value` or a `valueFrom`. The metric fields refer to an argument with the form `{{ args.name }}`.

- An argument with a `value` has a default. The Rollout can override it.
- An argument without a value must be set by the Rollout or the `AnalysisRun`. If it is missing, the run ends in the `Error` phase.
- `valueFrom` reads the value from a Secret (`secretKeyRef`) or from the Rollout (`fieldRef`). It keeps tokens out of the template.

The Rollout sets an argument in the `args` list of the analysis step. The step values override the defaults in the template.

## Metrics and how they are measured

The list `spec.metrics` holds one or more metrics. Each metric has a `name`, a `provider`, and fields that decide how often it runs and when it stops:

| Field | Meaning | Default |
| --- | --- | --- |
| `count` | Number of measurements to take | None |
| `interval` | Time between measurements, for example `30s` | None |
| `initialDelay` | Wait before the first measurement | 0 |
| `failureLimit` | Failed measurements allowed before the metric fails | 0 |
| `inconclusiveLimit` | Inconclusive measurements allowed before the metric is inconclusive | 0 |
| `consecutiveErrorLimit` | Errors in a row allowed before the metric errors | 4 |

If you set neither `count` nor `interval`, the metric takes one measurement. If you set `interval` without `count`, the metric runs until the analysis is stopped. This is the form used for a background analysis. If you set `count`, the metric ends after that many measurements.

A failed measurement is counted. With `failureLimit: 0`, the first failed measurement fails the metric. With `failureLimit: 2`, the metric fails at the third failed measurement. This lets a metric tolerate one or two bad samples.

## Conditions

Two fields turn a measured value into a result. The measured value is available as `result`.

- `successCondition` is an expression that must be true for a good measurement, for example `result == "200"` or `result[0] >= 0.95`.
- `failureCondition` is an expression that marks a bad measurement, for example `result[0] > 0.05`.

The rules are:

1. If only `successCondition` is set, a measurement that does not meet it is `Failed`.
2. If only `failureCondition` is set, a measurement that does not meet it is `Successful`.
3. If both are set, the measurement is `Failed` when the failure condition is true, `Successful` when the success condition is true, and `Inconclusive` when neither is true.
4. If neither is set, the measurement is `Successful` as long as the provider returned a value.

The `job` provider does not use conditions. The result of the Job decides: a Job that succeeds is `Successful` and a Job that fails is `Failed`.

<!-- astrona:playground:renew -->

## Writing a template

Save this as `analysis-template.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-status
  namespace: starfleet
spec:
  args:
  - name: status
    value: "200"
  metrics:
  - name: probe-ok
    count: 3
    interval: 10s
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

Apply it and read it back:

```sh
kubectl apply -f analysis-template.yaml
kubectl -n starfleet get analysistemplate probe-status -o yaml
```

The object exists but nothing runs. No Job pod appears until an `AnalysisRun` is created from it.

## Common pitfalls

> [!WARNING]
> A template holds no result. The result lives in the `AnalysisRun`. A `failureLimit` of 0 means one bad measurement fails the metric. An argument with no default and no value in the Rollout makes the run end in `Error`, not `Failed`.
