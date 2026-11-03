---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Complete A Canary Revision With Weight And Pause Steps

The `mission` Rollout replaces all pods at once. The team wants the new revision to take half of the pods first, wait briefly, and then take all of them.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-02-01" || exit 1
```

## Required result

- Update the Rollout `mission` with the canary steps: `setWeight: 50`, then `pause` with `duration: 5s`, then `setWeight: 100`.
- Release revision two by setting `REVISION` to `two` in the pod template.
- End state: the Rollout is `Healthy`, the new ReplicaSet is stable and 2 pods are updated and ready.

## Constraints

- Update the existing Rollout.
- Do not change the ConfigMap `initial-rollout`.
- This environment has no traffic router, so weights are replica ratios and not request percentages.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
