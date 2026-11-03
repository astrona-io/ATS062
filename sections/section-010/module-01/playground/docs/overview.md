---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Guided Practice: Rollout, ReplicaSets And Revisions

This exercise creates a Rollout, reads the ReplicaSet the controller creates, and then changes the pod template to create a second revision.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-010-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-010-01" || exit 1
```

Save the first revision. It has two replicas and the `canary` strategy without steps.

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

Then wait for the controller and list the objects it created. The Rollout is the owner of the ReplicaSet, and the ReplicaSet is the owner of the pods.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get rollout mission
kubectl -n starfleet get replicasets -l app=mission --show-labels
kubectl -n starfleet get replicasets -l app=mission -o jsonpath='{.items[*].metadata.ownerReferences[*].kind}'
```

Now change the pod template. The second file sets the environment variable `REVISION` to `two`. Any change to `spec.template` creates a new revision and a new ReplicaSet.

Save this as `rollout-mission-two.yaml`:

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
          value: two
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
kubectl apply -f rollout-mission-two.yaml
```

Then read the revision numbers. The annotation `rollout.argoproj.io/revision` is on the Rollout and on every ReplicaSet. The older ReplicaSet stays in the list, scaled to zero, so that a rollback is possible.

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.metadata.annotations}'
kubectl -n starfleet get replicasets -l app=mission -o custom-columns=NAME:.metadata.name,REVISION:.metadata.annotations.rollout\.argoproj\.io/revision,DESIRED:.spec.replicas
```

## Common pitfalls

> [!WARNING]
> The two ReplicaSets have different `rollouts-pod-template-hash` labels. Select pods by that label, not by `app` alone, when you need one revision.
