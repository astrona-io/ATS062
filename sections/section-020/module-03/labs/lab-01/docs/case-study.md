---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Starting Environment

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The Services `mission-stable` and `mission-canary` and the Ingress `mission-ingress` exist. The Rollout has no steps and no traffic routing. The cluster has no NGINX Ingress controller, so the check reads the objects only.
