---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Guided Practice: NGINX Traffic Routing

This exercise lets the Rollouts controller create a canary Ingress and reads its annotations.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-020-03)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-020-03" || exit 1
```

Save the Rollout with the NGINX traffic routing and the two steps.

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
      stableService: mission-stable
      canaryService: mission-canary
      trafficRouting:
        nginx:
          stableIngress: mission-ingress
          additionalIngressAnnotations:
            canary-by-header: X-Canary
      steps:
      - setWeight: 20
      - pause: {}
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the result:

```sh
kubectl -n starfleet get ingress
kubectl -n starfleet get ingress mission-mission-ingress-canary -o jsonpath='{.metadata.annotations}{"\n"}'
```

## Common pitfalls

> [!WARNING]
> The playground has no NGINX Ingress controller, so the annotations are written but no proxy uses them.
