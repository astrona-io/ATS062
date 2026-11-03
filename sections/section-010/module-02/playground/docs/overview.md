---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Guided Practice: Migrate A Deployment With workloadRef

This exercise adopts an existing Deployment named `crew` with a Rollout, and then reads the status fields the controller writes.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-010-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-010-02" || exit 1
```

Inspect the Deployment first. It has 2 replicas and serves the `crew` Service.

```sh
kubectl -n starfleet get deployment crew
kubectl -n starfleet get endpoints crew
```

Now write a Rollout that points at it. The Rollout has no `template`; it reads the template of `crew`.

Save this as `rollout-crew.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: crew-rollout
  namespace: starfleet
spec:
  replicas: 2
  workloadRef:
    apiVersion: apps/v1
    kind: Deployment
    name: crew
    scaleDown: onsuccess
  strategy:
    canary: {}
```

Apply it:

```sh
kubectl apply -f rollout-crew.yaml
```

Then watch the hand-over. The status shows the phase and the ReplicaSet counters, and the Deployment is scaled down after the Rollout is `Healthy`.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/crew-rollout --timeout=240s
kubectl -n starfleet get rollout crew-rollout -o jsonpath='{.status}'
kubectl -n starfleet get deployment crew
kubectl -n starfleet get endpoints crew
```

## Common pitfalls

> [!WARNING]
> Applying a change to the Deployment template starts a new revision of the Rollout. The Deployment itself no longer creates pods, so its own rollout status is not the evidence to read.
