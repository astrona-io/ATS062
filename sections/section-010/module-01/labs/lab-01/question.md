---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Reconcile A Rollout And Its ReplicaSet

The `starfleet` team wants the `mission` workload managed by Argo Rollouts instead of a Deployment.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. No Rollout exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-01-01" || exit 1
```

## Required result

- Create a Rollout named `mission` in `starfleet` with 2 replicas, the `canary` strategy without steps, and `revisionHistoryLimit: 3`.
- Use the image `docker.io/library/python:3.13-alpine`, the label `app: mission`, port 8080 and the command `python -m http.server 8080`.
- Wait until the Rollout is `Healthy` and the ReplicaSet created by the controller has 2 ready pods.

## Constraints

- Do not create a Deployment named `mission`.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
