---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# AnalysisTemplates And Metric Providers

An analysis lets the Rollouts controller decide with measurements whether a release is healthy. This module covers the reusable definition: the `AnalysisTemplate`, its arguments, the fields that control how often and how strictly a metric is measured, and the providers that take the measurement.

## Learning Goals

- Explain the difference between an `AnalysisTemplate`, a `ClusterAnalysisTemplate` and an `AnalysisRun`.
- Write a template with arguments and a metric with `count`, `interval`, `successCondition` and `failureLimit`.
- Choose between the `job`, `web` and `prometheus` providers.
- Predict whether a measurement is `Successful`, `Failed`, `Inconclusive` or `Error`.

## Before You Start

You need to know the `Rollout` resource and the canary steps. The playground has the Argo Rollouts controller and the `probe` Service in the `starfleet` namespace.

## Reading Order

1. The template, its arguments and its metrics.
2. Providers and measurement results.
3. Summary.

<!-- astrona:playground -->
