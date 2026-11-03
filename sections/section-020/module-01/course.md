---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Blue-Green Deployments

A blue-green release runs the old and the new version at full size next to each other, and then moves all traffic in one step. This module explains how Argo Rollouts does it with two Services, which settings decide when the switch happens, and how a failed release returns to the old version.

## Learning Goals

- Explain the roles of `activeService` and `previewService` and how the controller changes their selectors.
- Set `autoPromotionEnabled`, `autoPromotionSeconds`, `scaleDownDelaySeconds` and `previewReplicaCount`.
- Place analysis before and after the switch with `prePromotionAnalysis` and `postPromotionAnalysis`.
- Describe what happens to the old ReplicaSet after promotion and after an abort.

## Before You Start

You need to know what a Service selector is, what `rollouts-pod-template-hash` labels, and the fields `stableRS` and `currentPodHash`. The playground has the Argo Rollouts controller installed.

## Reading Order

1. Active and preview Services.
2. Promotion, analysis hooks and rollback.
3. Summary.

<!-- astrona:playground -->
