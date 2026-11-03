---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Starting Environment

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Two healthy Rollouts exist at revision `one`: `scout` (blue-green, Services `scout-active` and `scout-preview`) and `mission` (canary, no steps). The ConfigMap `initial-mission` records the hash of revision one of `mission`.
