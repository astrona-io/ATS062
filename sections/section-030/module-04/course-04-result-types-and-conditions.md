---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Result Types And Conditions

A condition is an expression that the controller evaluates against the value a provider returned. A wrong assumption about the type of the value makes a correct service look broken. This part shows the type of `result` for each provider and how the three condition fields interact.

## The type of result

The controller evaluates the conditions with an expression language. The variable `result` has the type that the provider returned.

| Provider | Type of result | Example condition |
| --- | --- | --- |
| `web` with `jsonPath` | The selected JSON value | `result == 200` |
| `web` without `jsonPath` | The whole JSON object | `result.status == 200` |
| `prometheus` | A list of numbers | `result[0] >= 0.95` |
| `datadog` | A list of numbers | `result[0] < 0.05` |
| `job` | None | The Job exit code decides |

A `job` metric has no conditions, since the phase of the Job is the result. A condition on a `job` metric is not used.

## Three condition fields

The metric can have `successCondition`, `failureCondition` or both. The controller evaluates them in this order for each measurement:

1. If `failureCondition` is true, the measurement fails.
2. Else if `successCondition` is true, the measurement succeeds.
3. Else, if both fields exist, the measurement is inconclusive.
4. If only `successCondition` exists and is false, the measurement fails.

Use both fields when a value can be good, bad or in between. For a latency metric, a `successCondition` of `result[0] < 0.2` and a `failureCondition` of `result[0] > 0.5` give three outcomes. A value of 0.3 is inconclusive, and `inconclusiveLimit` decides how many of these the run accepts.

## Testing a condition

<!-- astrona:playground:renew -->

A good habit is to read what a finished run recorded before trusting a condition. Read the counters of every run in the namespace:

```sh
kubectl -n starfleet get analysisruns -o jsonpath='{range .items[*]}{.metadata.name} {.status.metricResults[0].successful} {.status.metricResults[0].failed} {.status.metricResults[0].error}{"\n"}{end}'
```

The three numbers are the counts of successful, failed and error measurements for the metric. An error count above zero shows that the provider could not give a value at all.

## Type mistakes

The most common mistakes follow from the type.

- Comparing a list to a number: `result >= 0.95` on a Prometheus answer is a type error. Use `result[0]`.
- Comparing a string to a number: a value in quotes does not equal a number.
- Reading a field that is missing: `result.status` on a body without that field is an error measurement.

An error measurement is not a failed one. It counts toward `consecutiveErrorLimit` and not toward `failureLimit`, so a typing mistake aborts the release only after the error limit passes.

## What you know now

The type of `result` follows the provider, and the success and failure conditions combine into three outcomes. A mistake in the type shows as an error. The module closes with its main points.

## Common pitfalls

> [!WARNING]
> A `successCondition` alone turns every value outside the condition into a failure, so a noisy metric fails often. Add a `failureCondition` and let the values between the two be inconclusive when a small difference is not a defect.
