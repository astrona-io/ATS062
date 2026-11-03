---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Dry Run, Retention And Error Handling

A new metric is risky. If its query is wrong, it fails every release, and the team learns about it only when a release aborts. An `AnalysisRun` also stores each measurement, and a long run can grow large. This part covers the template settings that test a metric safely, limit stored data, and separate a failed check from a broken one.

## Failure, inconclusive and error

Three outcomes of a measurement look similar and mean different things. A `Failed` measurement is a value that broke the condition: the application is bad. An `Inconclusive` measurement is a value that met neither the success nor the failure condition: the data cannot decide. An `Error` measurement means the provider could not measure at all: the query timed out, the service was not reachable or the result could not be read.

Each outcome has its own limit. `failureLimit` counts failed measurements. `inconclusiveLimit` counts inconclusive ones. `consecutiveErrorLimit` counts errors in a row, with a default of 4. An error followed by a good measurement resets the counter. When a limit is exceeded, the metric takes the matching phase, and the `AnalysisRun` takes the phase of the metric.

## Dry run

The field `spec.dryRun` lists metrics that run but cannot fail the `AnalysisRun`. Each entry has a `metricName`, which can be a regular expression. The controller records the results of a dry-run metric in the run, with the phase of the metric, and ignores them when it decides the phase of the whole run.

Save this as `analysistemplate-dry-run.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: dry-run-demo
  namespace: starfleet
spec:
  dryRun:
  - metricName: experimental-.*
  metrics:
  - name: stable-check
    count: 1
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
                command: ["python", "-c", "print('ok')"]
  - name: experimental-check
    count: 1
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
                command: ["python", "-c", "raise SystemExit(1)"]
```

Apply it:

<!-- astrona:playground:renew -->

```sh
kubectl apply -f analysistemplate-dry-run.yaml
```

The metric `experimental-check` always fails. In a run created from this template, it fails in the record, and the run still ends `Successful`, because only `stable-check` counts. This is how a team tries a new metric on real releases before it lets the metric stop them.

## Measurement retention

The field `spec.measurementRetention` limits how many measurements an `AnalysisRun` keeps for a metric. Each entry has a `metricName` (a regular expression is allowed) and a `limit`. When the number of measurements passes the limit, the controller drops the oldest. A background metric that measures every 30 seconds for hours would otherwise store thousands of entries in the status of one object.

```yaml
  measurementRetention:
  - metricName: .*
    limit: 20
```

The snippet belongs at the top level of the template `spec`. It keeps the last 20 measurements of every metric.

## What you know now

A broken measurement is an error, an undecided one is inconclusive and a bad one is a failure, and each has its own limit. A dry-run metric records without deciding, and retention caps stored measurements. The next module follows an `AnalysisRun` inside a release.

## Common pitfalls

> [!WARNING]
> A dry-run metric that always errors hides a broken query forever, because nothing stops the release. Read the recorded results of dry-run metrics during the trial. Retention drops old measurements from the status, so use it with care when a postmortem needs the full history.
