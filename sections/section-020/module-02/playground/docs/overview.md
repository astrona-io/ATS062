---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Guided Practice: Canary Steps

This exercise releases a second revision through canary steps and reads the step index while the Rollout moves.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-020-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-020-02" || exit 1
```

Check the starting point. The Rollout has no steps, and its stable ReplicaSet is revision one.

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.status.stableRS} {.status.phase}'
```

Save the second revision with three steps: 25 percent, a 20 second pause, and 100 percent.

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
      - setWeight: 25
      - pause:
          duration: 20s
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then read the progress while it runs. `currentStepIndex` is the index of the step the controller works on. During the pause, `phase` is `Paused`.

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentStepIndex} {.status.phase}'
kubectl -n starfleet get replicasets -l app=mission
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
```

## Common pitfalls

> [!WARNING]
> With 2 replicas, 25 percent rounds up to 1 canary pod. Small replica counts make the real ratio differ from the declared weight.
