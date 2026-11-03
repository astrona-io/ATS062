---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Set Timing Fields And Stable Metadata On A Rollout

The `starfleet` team wants a `relay` workload that waits before it counts pods as available and labels its stable pods.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-01-02" || exit 1
```

## Required result

- Create a Rollout named `relay` in `starfleet` with 2 replicas, `minReadySeconds: 5`, `progressDeadlineSeconds: 120` and `revisionHistoryLimit: 2`.
- Use the `canary` strategy with `stableMetadata` that sets the label `role: stable`.
- Use the image `docker.io/library/python:3.13-alpine`, the label `app: relay`, port 8080 and the command `python -m http.server 8080`.
- Wait until the Rollout is `Healthy` and its 2 pods carry the label `role: stable`.

## Constraints

- Do not create a Deployment named `relay`.
- Do not put the label `role` in the pod template.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
