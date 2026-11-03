---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Strategies Capstone: Preview A Blue-Green Release And Complete A Canary Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-cap-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-cap-01" || exit 1
```

Write the blue-green change for `scout`.

Save this as `rollout-scout.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: scout
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: scout
  template:
    metadata:
      labels:
        app: scout
    spec:
      containers:
      - name: scout
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
    blueGreen:
      activeService: scout-active
      previewService: scout-preview
      autoPromotionEnabled: false
```

Apply it:

```sh
kubectl apply -f rollout-scout.yaml
```

Then write the canary change for `mission`.

Save this as `rollout-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 2
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
    canary:
      steps:
      - setWeight: 50
      - pause:
          duration: 5s
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then wait and check both. `scout` stays `Paused`; `mission` reaches `Healthy`.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Paused rollout/scout --timeout=240s
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get rollouts
```

## Verify the result

`scout` shows `Paused`, `stableRS` differs from `currentPodHash`, and the Services select the matching hashes. `mission` shows `Healthy` with `stableRS` equal to `currentPodHash` and a different hash than `initial-mission`.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-cap-01`.

## Common pitfalls

> [!WARNING]
> Both Rollouts use the label `app` with different values. Check each Rollout with its own label; a combined selector mixes the pods of the two workloads.
