---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Strategies Capstone: Preview A Blue-Green Release And Complete A Canary

Two workloads release a new revision today. `scout` must wait in preview for review. `mission` must move through canary steps by itself.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Two healthy Rollouts exist at revision `one`: `scout` (blue-green, Services `scout-active` and `scout-preview`) and `mission` (canary, no steps). The ConfigMap `initial-mission` records the hash of revision one of `mission`.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-cap-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-cap-01" || exit 1
```

## Required result

- `scout`: set `previewService: scout-preview`, `autoPromotionEnabled: false`, release `REVISION=two`, and leave it waiting in preview (`Paused`). `scout-active` must still select revision one.
- `mission`: add the steps `setWeight: 50`, `pause` for `5s`, `setWeight: 100`, release `REVISION=two`, and let it finish `Healthy` with the new ReplicaSet stable.

## Constraints

- Update the existing Rollouts.
- Do not promote `scout`.
- Do not change the ConfigMap `initial-mission`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
