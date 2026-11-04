---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Autoscale A Rollout With An HPA Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-04-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-04-01" || exit 1
```

The utilization target is a percentage of the CPU request, so the Rollout needs a request first.

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
kubectl -n starfleet get hpa mission-hpa -o jsonpath='{.spec.scaleTargetRef}{"\n"}'
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase}{"\n"}'
```

## Verify the result

The grader reads the autoscaler fields, the CPU request in the pod template and the Rollout status. It does not require a metrics server.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-04-01`.

## Common pitfalls

> [!WARNING]
> Without a CPU request the autoscaler cannot compute a utilization. Without a metrics server in the cluster, the autoscaler status shows unknown values, but the fields are still valid.
