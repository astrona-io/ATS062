---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Reconcile A Rollout And Its ReplicaSet Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-01-01" || exit 1
```

Write the Rollout. The `strategy.canary` field selects the canary strategy. An empty `canary: {}` has no steps, so the new ReplicaSet receives the whole workload at once.

Save this as `rollout-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 2
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: mission
  template:
    metadata:
      labels:
        app: mission
    spec:
      containers:
      - name: mission
        image: docker.io/library/python:3.13-alpine
        env:
        - name: REVISION
          value: one
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary: {}
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the objects. The controller creates the ReplicaSet, and the ReplicaSet creates the pods.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get rollout mission
kubectl -n starfleet get replicasets -l app=mission --show-labels
```

## Verify the result

The Rollout shows phase `Healthy`. One ReplicaSet owned by the Rollout carries the label `rollouts-pod-template-hash` with the same value as `status.currentPodHash`, and it has 2 ready pods. No Deployment named `mission` exists.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-01-01`.

## Common pitfalls

> [!WARNING]
> A Rollout never creates a Deployment. If you apply a Deployment by habit, the grader fails because the ReplicaSets must be owned by a Rollout.
