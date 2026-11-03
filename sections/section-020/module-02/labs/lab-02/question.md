---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Limit Surge And Unavailability In A Canary

The `starfleet` team wants a `relay` workload with four replicas that never loses a pod during a release.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-02-02" || exit 1
```

## Required result

- Create a Rollout named `relay` in `starfleet` with 4 replicas and the `canary` strategy.
- Set `maxSurge: 1` and `maxUnavailable: 0` and the steps `setWeight: 50`, a `pause` of 5 seconds and `setWeight: 100`.
- Use the image `docker.io/library/python:3.13-alpine`, the label `app: relay`, port 8080 and the command `python -m http.server 8080`.
- Wait until the Rollout is `Healthy` with 4 ready pods.

## Constraints

- Do not create a Deployment named `relay`.
- Do not use `trafficRouting`.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
