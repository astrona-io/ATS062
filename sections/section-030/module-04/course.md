---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Analysis Providers In Depth

The `job` provider can run any check, but most teams measure with the monitoring system they already have. This module explains the `web` provider, the `prometheus` provider and the vendor providers, and how the shape of the result decides how a condition is written.

## Learning Goals

- Write a `web` metric with `url`, `jsonPath` and a condition.
- Write a `prometheus` metric and explain why its result is a list.
- Name the vendor providers and the secret each one reads.
- Write a success and a failure condition that matches the type of the result.

## Before You Start

You need to know an `AnalysisTemplate`, its arguments and the `count`, `interval` and `failureLimit` fields. The playground has the controller and the `probe` Service. The `probe` Service answers `/work?status=200` with a JSON body that has the field `status`. The playground has no Prometheus and no vendor service.

## Reading Order

1. The web provider.
2. The Prometheus provider.
3. Vendor providers and plugins.
4. Result types and conditions.
5. Summary.

<!-- astrona:playground -->
