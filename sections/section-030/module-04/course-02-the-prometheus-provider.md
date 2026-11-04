---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# The Prometheus Provider

Prometheus is a monitoring system that stores time series and answers queries in its own language, PromQL. The `prometheus` provider runs a PromQL query for each measurement. This part shows the fields and the shape of the answer, which differs from the `web` provider.

## The fields

The provider needs an `address`, the URL of the Prometheus server, and a `query`. It may set `timeout` in seconds, `insecure` to skip the certificate check, and `headers` for extra request headers. The `authentication` block holds the settings for OAuth 2.0 or for AWS signing, when the server needs them. Arguments are used inside the query, for example to choose the canary pods:

```yaml
metrics:
- name: success-rate
  interval: 1m
  successCondition: result[0] >= 0.95
  failureLimit: 3
  provider:
    prometheus:
      address: http://prometheus.monitoring.svc.cluster.local:9090
      query: |
        sum(rate(http_requests_total{service="{{ args.service }}",code!~"5.."}[2m]))
        /
        sum(rate(http_requests_total{service="{{ args.service }}"}[2m]))
```

<!-- astrona:playground:renew -->

The playground has no Prometheus server, so this example cannot run. Check the fields with `kubectl explain`, which reads them from the CRD:

```sh
kubectl explain analysistemplate.spec.metrics.provider.prometheus
kubectl explain analysistemplate.spec.metrics.provider.prometheus.authentication
```

## The result is a list

A PromQL query returns a vector: a list of values, one for each time series that matches. The provider gives this list to the condition as `result`. A query with one series gives a list with one number, so the condition reads `result[0]`. A query that matches no series gives an empty list, and `result[0]` is then an error, which the controller records as an error measurement.

For this reason a query usually ends with an aggregation such as `sum(...)`, so exactly one value comes back. The division of two sums in the example returns a single ratio.

## Measuring the right pods

A metric for the whole Service mixes the stable and the canary pods. During a canary, the numbers of the stable version can hide a problem in the canary. A better query selects the canary pods by a label. The Rollout can pass the hash of the canary ReplicaSet as an argument through `valueFrom.podTemplateHashValue`, and the query filters on the label `rollouts_pod_template_hash`. This compares what the canary does and not what the average does.

## Timing

Prometheus computes rates over a window, such as `[2m]`. A metric measured 10 seconds after the canary starts sees a window mostly filled by the stable version. Use `initialDelay` on the metric to let the window fill before the first measurement.

## What you know now

The `prometheus` provider runs a PromQL query and returns a list. Queries aggregate to one value, conditions read `result[0]`, and arguments select the canary pods. The next question is what other providers exist.

## Common pitfalls

> [!WARNING]
> A query with no matching series returns an empty list and the measurement is an error. A rate over a window that is longer than the time the canary has run reports mostly the stable version. A very low `interval` can overload the Prometheus server.
