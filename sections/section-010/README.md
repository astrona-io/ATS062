---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Understand Argo Rollouts Fundamentals

This section explains what the Argo Rollouts controller adds to a Deployment. It covers the Rollout resource, the ReplicaSets and hashes that track revisions, the status fields that show the state of a release, and the migration of a running Deployment with workloadRef.

## Modules

1. Rollout Resource, ReplicaSets And Revisions
2. Operating Rollouts And Migrating From A Deployment

Each module has a short landing page, two parts and a summary. A playground and a graded lab follow the parts. The section ends with a capstone lab and a knowledge check.

## Learning Outcomes

- Distinguish a Rollout from a Deployment and name what the controller owns.
- Read the pod template hash, stableRS, currentPodHash and revisionHistoryLimit.
- Read the phase and conditions of a release, and pause, abort or promote it.
- Migrate a Deployment to a Rollout with workloadRef and scaleDown.
