---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Run A Blue-Green Rollout With A Small Preview

The `starfleet` team wants a blue-green `relay` workload with active and preview Services and role labels on the active pods.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-02" || exit 1
```

## Required result

- Create the Services `relay-active` and `relay-preview` in `starfleet`, both selecting `app: relay` on port 8080.
- Create a Rollout named `relay` with 2 replicas and the `blueGreen` strategy that uses those two Services, `previewReplicaCount: 1`, `scaleDownDelaySeconds: 45` and `activeMetadata` with the label `role: active`.
- Use the image `docker.io/library/python:3.13-alpine`, the label `app: relay`, port 8080 and the command `python -m http.server 8080`.
- Wait until the Rollout is `Healthy` and `relay-active` selects the stable ReplicaSet.

## Constraints

- Do not create a Deployment named `relay`.
- Do not put the label `role` in the pod template.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
