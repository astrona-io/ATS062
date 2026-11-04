---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Configure The Controller Log Level And Format

The `argo-rollouts` controller log is hard to feed into a log collector, and a fault in the `starfleet` namespace needs more detail. Change how the controller logs.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The controller Deployment `argo-rollouts` runs with its default arguments.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-03-01" || exit 1
```

## Required result

- Patch the Deployment `argo-rollouts` in the namespace `argo-rollouts` so the container `argo-rollouts` runs with `--loglevel debug` and `--logformat json`.
- End state: the Deployment has finished its rollout and the new controller pod is ready.

## Constraints

- Patch the existing Deployment. Do not delete it and do not change its name.
- Do not change the namespace or the image.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
