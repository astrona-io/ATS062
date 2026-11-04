---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Experiments

An `AnalysisRun` measures a release that is already receiving traffic. An `Experiment` runs temporary pods on their own, so a team can compare versions and measure them before any user is affected. This module explains the `Experiment` resource, its analyses, its use inside a canary and how to debug it.

## Learning Goals

- Describe the fields of an `Experiment` and its phases.
- Attach analyses to an experiment and use `requiredForCompletion`.
- Add an `experiment` step to a canary and use `specRef`.
- Read the status of an experiment and find the reason for a failure.

## Before You Start

You need to know an `AnalysisTemplate` and the phases of an `AnalysisRun`. The playground has the controller, the `probe` Service and an `AnalysisTemplate` named `probe-gate` with the argument `status`.

## Reading Order

1. The Experiment resource.
2. Analyses inside an experiment.
3. Experiments in a canary.
4. Reading and debugging an experiment.
5. Summary.

<!-- astrona:playground -->
