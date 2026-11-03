---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Migrate A Deployment To A Rollout With workloadRef

The `cargo` Deployment in `starfleet` serves traffic through the `cargo` Service. The team wants Argo Rollouts to manage it without rewriting the Deployment.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. A Deployment named `cargo` (2 replicas, label `app: cargo`) and a Service named `cargo` already exist and are ready.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-02-01" || exit 1
```

## Required result

- Create a Rollout named `cargo-rollout` in `starfleet` that references the Deployment `cargo` with `workloadRef`, with 2 replicas and the `canary` strategy without steps.
- Set `scaleDown` to `onsuccess` so the controller scales the Deployment to 0 after the Rollout is healthy.
- The `cargo` Service must keep 2 ready endpoints.

## Constraints

- Do not copy the pod template into the Rollout.
- Do not delete the Deployment or the Service.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
