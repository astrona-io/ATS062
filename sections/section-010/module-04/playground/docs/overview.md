---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Guided Practice: Autoscaling A Rollout

This exercise points an autoscaler at a Rollout and reads the scale subresource.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-010-04)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-010-04" || exit 1
```

Save the Rollout with a CPU request and revision two.

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
        resources:
          requests:
            cpu: 50m
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

Save the autoscaler that targets the Rollout.

Save this as `hpa-mission.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mission-hpa
  namespace: starfleet
spec:
  scaleTargetRef:
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    name: mission
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply it:

```sh
kubectl apply -f hpa-mission.yaml
```

Then check the result:

```sh
kubectl -n starfleet get hpa mission-hpa
kubectl -n starfleet get rollout mission -o jsonpath='{.status.replicas} {.status.selector}{"\n"}'
```

## Common pitfalls

> [!WARNING]
> A cluster without a metrics server shows `<unknown>` as the current utilization. The autoscaler object is still correct.
