---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Canary Deployments

A canary release sends a growing share of the work to the new version in steps, and waits between the steps. This module explains how the steps run, how the controller turns a weight into a number of pods, what a traffic router changes, and how a canary is paused, promoted and aborted.

## Learning Goals

- Write canary steps with `setWeight` and `pause`, and predict the replica counts they produce.
- Explain how `maxSurge` and `maxUnavailable` shape a canary without a router.
- Explain what `trafficRouting`, `stableService` and `canaryService` add.
- Choose between a canary and a blue-green strategy for a given workload.

## Before You Start

You need to know what a `Rollout`, `stableRS` and `currentPodHash` are, and how a Service selects pods. The playground has the Argo Rollouts controller installed.

## Reading Order

1. Steps, weights and replica counts.
2. Traffic routing, controlling a canary and choosing a strategy.
3. Summary.

<!-- astrona:playground -->
