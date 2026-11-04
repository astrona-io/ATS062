---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Route A Canary Through An NGINX Ingress

External requests for `mission` enter through the Ingress `mission-ingress`. The canary must receive 20 percent of them, and requests with the header `X-Canary` must reach it.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The Services `mission-stable` and `mission-canary` and the Ingress `mission-ingress` exist. The Rollout has no steps and no traffic routing. The cluster has no NGINX Ingress controller, so the check reads the objects only.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-03-01" || exit 1
```

## Required result

- Update the Rollout `mission` to use `stableService: mission-stable`, `canaryService: mission-canary` and `trafficRouting.nginx.stableIngress: mission-ingress`.
- Add the canary annotation `canary-by-header: X-Canary` through `additionalIngressAnnotations`.
- Use the steps `setWeight: 20` and an open `pause: {}`, and release `REVISION=two`.
- End state: the Rollout is `Paused` at the pause step, and the canary Ingress `mission-mission-ingress-canary` that the controller created has `canary: "true"`, `canary-weight: "20"` and `canary-by-header: X-Canary`.

## Constraints

- Update the existing Rollout.
- Do not create or edit the canary Ingress yourself.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
