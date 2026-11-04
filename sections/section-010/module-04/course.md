---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Scaling A Rollout With Autoscalers

A production workload changes size with load. This module explains how a `Rollout` exposes its replica count to autoscalers, how a HorizontalPodAutoscaler (HPA) controls a `Rollout`, how a release behaves while the replica count changes, and how scheduling rules keep old and new pods apart.

## Learning Goals

- Explain the scale subresource and what `kubectl scale` changes on a `Rollout`.
- Write an HPA whose `scaleTargetRef` is a `Rollout`.
- Describe how canary weights and blue-green sets follow a changing replica count.
- Describe anti-affinity settings and a PodDisruptionBudget for a `Rollout`.

## Before You Start

You need to know what a `Rollout`, a ReplicaSet and a canary weight are. The playground has the controller and a healthy `Rollout` named `mission` with two replicas. The playground has no metrics server, so the HPA cannot read real load.

## Reading Order

1. The scale subresource and the replica count.
2. An HPA that targets a Rollout.
3. Releases while the replica count changes.
4. Anti-affinity, disruption budgets and other autoscalers.
5. Summary.

<!-- astrona:playground -->
