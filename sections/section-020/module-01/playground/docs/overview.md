---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Guided Practice: Blue-Green Active And Preview Services

This exercise creates a blue-green Rollout with two Services, and then releases a second revision that waits in preview.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-020-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-020-01" || exit 1
```

Save the first revision. It creates the two Services and a blue-green Rollout with automatic promotion. The first revision has no earlier revision to protect, so it becomes active at once.

Save this as `bluegreen-mission.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: active
  namespace: starfleet
spec:
  selector:
    app: mission
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: preview
  namespace: starfleet
spec:
  selector:
    app: mission
  ports:
  - port: 8080
    targetPort: 8080
---
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
          value: one
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    blueGreen:
      activeService: active
      previewService: preview
      autoPromotionEnabled: true
```

Apply it:

```sh
kubectl apply -f bluegreen-mission.yaml
```

Then read the selector the controller added to the active Service.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get service active -o jsonpath='{.spec.selector}'
kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash}'
```

Now release revision two with `autoPromotionEnabled: false`.

Save this as `rollout-mission-two.yaml`:

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
    blueGreen:
      activeService: active
      previewService: preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 60
```

Apply it:

```sh
kubectl apply -f rollout-mission-two.yaml
```

Then compare the Services again. The Rollout stays paused until someone promotes it.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Paused rollout/mission --timeout=240s
kubectl -n starfleet get service active -o jsonpath='{.spec.selector}'
kubectl -n starfleet get service preview -o jsonpath='{.spec.selector}'
kubectl -n starfleet get replicasets -l app=mission
```

## Common pitfalls

> [!WARNING]
> The preview Service only has endpoints once the new pods are ready. An empty Endpoints list right after the apply is normal for a few seconds.
