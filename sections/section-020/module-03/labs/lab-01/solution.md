---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Route A Canary Through An NGINX Ingress Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-03-01" || exit 1
```

The Rollouts controller creates the canary Ingress when the Rollout reaches its first weight step.

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
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.currentStepIndex}{"\n"}'
kubectl -n starfleet get ingress mission-mission-ingress-canary -o jsonpath='{.metadata.annotations}{"\n"}'
```

## Verify the result

The grader reads the Rollout fields, the Rollout status and the annotations of the canary Ingress.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-03-01`.

## Common pitfalls

> [!WARNING]
> In `additionalIngressAnnotations` the key is written without the NGINX prefix. The stable Ingress must use the stable Service as backend, or the controller rejects the Rollout.
