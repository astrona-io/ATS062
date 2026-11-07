---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Gate A Blue-Green Switch And Set The Canary Scale

Two workloads release a new revision today. `scout` may switch its active Service only after an analysis has passed. `mission` must run its canary with one pod and a traffic split through an NGINX Ingress.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Two healthy Rollouts exist at revision `one`: `scout` (blue-green, Services `scout-active` and `scout-preview`, automatic promotion) and `mission` (canary, no steps, no traffic routing). The AnalysisTemplate `probe-gate` in `starfleet` has one job metric `probe-ok` that requests `http://probe:8080/work?status=<status>`; its argument `status` has the default `"200"`. The Services `mission-stable` and `mission-canary` and the Ingress `mission-ingress` exist. The cluster has no NGINX Ingress controller, so the check reads the objects only. The ConfigMap `initial-mission` records the hash of revision one of `mission`.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-capstone-020)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-capstone-020" || exit 1
```

## Required result

- `scout`: set `previewService: scout-preview`, keep automatic promotion, and add `prePromotionAnalysis` that uses the template `probe-gate` with the argument `status` set to `"200"`. Release `REVISION=two` and let the controller promote it. End state: `scout` is `Healthy`, revision 2 is stable, `scout-active` selects the new ReplicaSet, and the Rollout owns a `Successful` AnalysisRun.
- `mission`: set `stableService: mission-stable`, `canaryService: mission-canary`, `trafficRouting.nginx.stableIngress: mission-ingress` and `dynamicStableScale: true`. Use the steps `setCanaryScale` with `replicas: 1`, `setWeight: 50`, `pause` for `10s` and `setWeight: 100`. Release `REVISION=two`. End state: `mission` is `Healthy` with the new ReplicaSet stable, and the canary Ingress `mission-mission-ingress-canary` that the controller created exists.

## Constraints

- Update the existing Rollouts.
- Do not promote `scout` by hand and do not create AnalysisRuns by hand.
- Do not create or edit the canary Ingress yourself.
- Do not change `probe-gate` or the ConfigMap `initial-mission`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
