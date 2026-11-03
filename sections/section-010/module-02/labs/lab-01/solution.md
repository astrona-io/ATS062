---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Migrate A Deployment To A Rollout With workloadRef Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-02-01" || exit 1
```

Write the Rollout. `workloadRef` replaces `spec.template`: the controller reads the pod template from the Deployment `cargo`.

Save this as `rollout-cargo.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: cargo-rollout
  namespace: starfleet
spec:
  replicas: 2
  workloadRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cargo
    scaleDown: onsuccess
  strategy:
    canary: {}
```

Apply it:

```sh
kubectl apply -f rollout-cargo.yaml
```

Then wait and check both objects. The Rollout creates its own pods. When it is `Healthy`, the controller sets the replicas of the Deployment to 0.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/cargo-rollout --timeout=240s
kubectl -n starfleet get deployment cargo
kubectl -n starfleet get endpoints cargo
```

## Verify the result

The Rollout is `Healthy` with 2 ready replicas. The Deployment `cargo` shows 0 desired replicas. The Endpoints object `cargo` lists 2 addresses, which are the pods of the Rollout.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-02-01`.

## Common pitfalls

> [!WARNING]
> With `scaleDown: never` the Deployment keeps running and both sets of pods receive traffic from the Service. Use `onsuccess` or `progressively` when the Deployment must stop.
