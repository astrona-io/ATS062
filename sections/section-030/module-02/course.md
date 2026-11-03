---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# AnalysisRuns And Rollout Integration

A Rollout uses analysis in three places: as a step in a canary, as a background check that runs beside the steps, and as a gate around a blue-green promotion. This module explains how the controller creates and watches an `AnalysisRun`, and how the result changes the Rollout.

## Learning Goals

- Describe the lifecycle of an `AnalysisRun` and its phases.
- Add an inline analysis step, a background analysis and a blue-green analysis to a Rollout.
- Explain how a `Failed`, `Inconclusive` and `Error` run change the Rollout.
- Describe what an `Experiment` adds to an analysis.

## Before You Start

You need to know `AnalysisTemplate` arguments, metrics and providers, and the canary steps. The playground has the controller, the `probe` Service and a healthy Rollout.

## Reading Order

1. The AnalysisRun lifecycle and the places a Rollout runs analysis.
2. How a result changes the Rollout, and Experiments.
3. Passing Rollout data into an analysis.
4. Reading and debugging an AnalysisRun.
5. Summary.

<!-- astrona:playground -->
