---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Rollout Resource, ReplicaSets And Revisions

This module explains what an Argo Rollouts `Rollout` is, which component acts on it, and how the objects around it (ReplicaSets, pods and revisions) fit together. It uses one running example: the `mission` workload in the `starfleet` namespace.

## Learning Goals

- Explain how a `Rollout` differs from a Kubernetes `Deployment` and which part of the spec is new.
- Name the component that creates ReplicaSets and pods, and the labels it adds.
- Read a revision number, the stable ReplicaSet and the current ReplicaSet from the status of a `Rollout`.
- State what `revisionHistoryLimit` keeps and why old ReplicaSets matter.

## Before You Start

You need basic Kubernetes knowledge: a pod runs containers, a ReplicaSet keeps a set number of identical pods, and a Deployment manages ReplicaSets. The playground has the Argo Rollouts controller installed. Commands use `kubectl` only.

## Reading Order

1. The Rollout resource and its controller.
2. ReplicaSets, hashes and revisions.
3. Timing, capacity and history fields.
4. Template changes, metadata and placement.
5. Summary.

<!-- astrona:playground -->
