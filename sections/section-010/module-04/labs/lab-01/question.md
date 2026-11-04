---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Autoscale A Rollout With An HPA

The `mission` Rollout in `starfleet` must follow CPU load between 2 and 5 replicas.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The pods of `mission` do not request CPU, and no HorizontalPodAutoscaler exists.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-04-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-04-01" || exit 1
```

## Required result

- Update the Rollout `mission` so its container requests `50m` CPU, and release `REVISION=two`.
- Create a HorizontalPodAutoscaler `mission-hpa` in `starfleet` that targets the Rollout `mission` through `argoproj.io/v1alpha1`, with `minReplicas: 2`, `maxReplicas: 5` and a CPU utilization target of 70 percent.
- End state: the Rollout is `Healthy` and the new ReplicaSet is stable.

## Constraints

- Update the existing Rollout.
- The HorizontalPodAutoscaler must use the API version `autoscaling/v2`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
