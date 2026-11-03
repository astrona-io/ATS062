---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Summary

A `Rollout` is a custom resource that replaces a Deployment as the owner of a workload. It has the same replicas, selector and pod template, and it adds a strategy of either `canary` or `blueGreen`. The Argo Rollouts controller acts on it. The controller creates ReplicaSets, scales them, updates Services and writes the progress into the status. Kubernetes still creates, schedules and runs the pods.

Each distinct pod template has its own ReplicaSet, named with a hash and labelled with `rollouts-pod-template-hash`. Each template change adds a revision number in the annotation `rollout.argoproj.io/revision`. The status field `currentPodHash` names the revision being rolled out, and `stableRS` names the last revision that finished. The `phase` is `Progressing`, `Paused`, `Healthy` or `Degraded`, and it is only current when `observedGeneration` matches the generation.

The setting `revisionHistoryLimit` decides how many old ReplicaSets remain. These ReplicaSets are the rollback targets, so removing them removes the fast way back.

The timing and history fields change what the controller does and never change the pods, so none of them starts a release. Only a change to the pod template starts one. Labels that only tell revisions apart belong in the metadata fields of the strategy, and `antiAffinity` keeps the two revisions on different nodes.

Key facts:

- The kind is `Rollout` in the group `argoproj.io`; its strategy is `canary` or `blueGreen`.
- The controller changes ReplicaSets and Services; the ReplicaSet controller creates pods.
- Only a pod template change creates a new ReplicaSet and revision.
- `stableRS` equals `currentPodHash` when no release is in progress.
- `minReadySeconds`, `progressDeadlineSeconds` and `revisionHistoryLimit` are not part of the pod template.
- `canaryMetadata` and `stableMetadata` label pods without a new revision.

<!-- astrona:playground:destroy -->
