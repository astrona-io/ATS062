---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Starting Environment

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The pods of `mission` do not request CPU, and no HorizontalPodAutoscaler exists.
