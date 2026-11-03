---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Fundamentals Capstone: Run And Update A Rollout Behind A Service

The `bridge` service must run as a Rollout behind the existing `bridge` Service, and it must already have been updated once.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. A Service named `bridge` (selector `app: bridge`, port 8080) exists. No workload backs it yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-cap-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-cap-01" || exit 1
```

## Required result

- Create a Rollout `bridge` in `starfleet` with 3 replicas, the label `app: bridge`, the `canary` strategy without steps, and `revisionHistoryLimit: 2`.
- Create revision 1 with the environment variable `REVISION=one`, then update the pod template to `REVISION=two`.
- End state: the Rollout is `Healthy`, revision 2 is current and stable, and the `bridge` Service has 3 ready endpoints.

## Constraints

- Update the same Rollout; do not delete and recreate it.
- Do not create a Deployment named `bridge`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
