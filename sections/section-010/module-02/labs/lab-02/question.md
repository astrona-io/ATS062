---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Set A Progress Deadline With Automatic Abort

The `starfleet` team wants a `beacon` workload whose release aborts by itself when it makes no progress.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-02-02" || exit 1
```

## Required result

- Create a Rollout named `beacon` in `starfleet` with 2 replicas and the `canary` strategy with the steps `setWeight: 50` and `pause` of 5 seconds.
- Set `progressDeadlineSeconds: 90` and `progressDeadlineAbort: true`.
- Use the image `docker.io/library/python:3.13-alpine`, the label `app: beacon`, port 8080 and the command `python -m http.server 8080`.
- Wait until the Rollout is `Healthy`.

## Constraints

- Do not create a Deployment named `beacon`.
- Do not pause the Rollout with `spec.paused`.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
