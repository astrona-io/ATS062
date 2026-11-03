---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Operating Rollouts And Migrating From A Deployment

This module covers how to read the state of a running `Rollout`, how to control a release that is in progress, and how to move an existing Deployment under Argo Rollouts. It also names the traffic management integrations that give exact request percentages.

## Learning Goals

- Read the `phase`, the conditions and the pause state of a `Rollout`.
- Name the commands that promote, abort, retry and undo a release.
- Migrate a Deployment with `workloadRef` and choose a `scaleDown` mode.
- Explain what a traffic router adds to a Service-based rollout.

## Before You Start

You need to know what a `Rollout`, a ReplicaSet and `status.stableRS` are. The playground has the Argo Rollouts controller installed. Hands-on steps use `kubectl` only.

## Reading Order

1. Reading status and controlling a release.
2. Migrating a Deployment and routing traffic.
3. Summary.

<!-- astrona:playground -->
