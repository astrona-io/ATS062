---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Fundamentals Capstone: Run And Update A Rollout Behind A Service Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-cap-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-cap-01" || exit 1
```

Write revision 1. The Service already selects `app: bridge`, so the pods join it when they are ready.

Save this as `rollout-bridge.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: bridge
  namespace: starfleet
spec:
  replicas: 3
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: bridge
  template:
    metadata:
      labels:
        app: bridge
    spec:
      containers:
      - name: bridge
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
kubectl apply -f rollout-bridge.yaml
```

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/bridge --timeout=240s
```

Then change the pod template. Only `REVISION` changes. Apply the new file over the same Rollout.

Save this as `rollout-bridge-two.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: bridge
  namespace: starfleet
spec:
  replicas: 3
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: bridge
  template:
    metadata:
      labels:
        app: bridge
    spec:
      containers:
      - name: bridge
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
kubectl apply -f rollout-bridge-two.yaml
```

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/bridge --timeout=240s
kubectl -n starfleet get rollout bridge -o jsonpath='{.metadata.annotations}'
kubectl -n starfleet get replicasets -l app=bridge
kubectl -n starfleet get endpoints bridge
```

## Verify the result

The annotation `rollout.argoproj.io/revision` on the Rollout is `2`. `status.stableRS` equals `status.currentPodHash`. The Rollout reports 3 ready replicas and the Endpoints object `bridge` lists 3 addresses.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-cap-01`.

## Common pitfalls

> [!WARNING]
> Applying the revision 2 file before revision 1 is healthy skips a revision: the annotation then reads 1, not 2. Wait for `Healthy` between the two applies.
