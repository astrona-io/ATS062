---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Summary

The `web` provider sends an HTTP request from the controller and reads JSON. The field `jsonPath` selects one value, and `result` holds that value in the conditions. The address must be reachable from the controller pod, so it uses the full Service name.

The `prometheus` provider runs a PromQL query. The answer is a list, so conditions read `result[0]`, and queries aggregate to one value. An empty answer is an error. Arguments select the canary pods, and `initialDelay` lets the rate window fill.

Vendor providers cover Datadog, New Relic, CloudWatch, Graphite, InfluxDB, Wavefront, SkyWalking and Kayenta. They read credentials from Secrets or from the identity of the controller pod. A plugin registered under `metricProviderPlugins` adds other sources.

The condition fields give three outcomes. A true `failureCondition` fails the measurement, a true `successCondition` succeeds, and a value that meets neither is inconclusive when both fields exist. A type mistake in a condition records an error and not a failure.

Key facts:

- A `job` metric has no condition; the Job result decides.
- Prometheus and Datadog results are lists.
- Errors count toward `consecutiveErrorLimit`.
- `insecure: true` removes certificate checks.

<!-- astrona:playground:destroy -->
