---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Starting Environment

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Two healthy Rollouts exist at revision `one`: `scout` (blue-green, Services `scout-active` and `scout-preview`, automatic promotion) and `mission` (canary, no steps, no traffic routing). The AnalysisTemplate `probe-gate` in `starfleet` has one job metric `probe-ok` that requests `http://probe:8080/work?status=<status>`; its argument `status` has the default `"200"`. The Services `mission-stable` and `mission-canary` and the Ingress `mission-ingress` exist. The cluster has no NGINX Ingress controller. The ConfigMap `initial-mission` records the hash of revision one of `mission`.
