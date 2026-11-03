---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Limit Surge And Unavailability In A Canary Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-02-02" || exit 1
```

With `maxUnavailable: 0` the controller must create a new pod before it removes an old one, and `maxSurge: 1` allows one pod above the replica count while it does so.

Save this as `rollout-relay.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: relay
  namespace: starfleet
spec:
  replicas: 4
  selector:
    matchLabels:
      app: relay
  template:
    metadata:
      labels:
        app: relay
    spec:
      containers:
      - name: relay
        image: docker.io/library/python:3.13-alpine
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary:
      maxSurge: 1
      maxUnavailable: 0
      steps:
      - setWeight: 50
      - pause: {duration: 5s}
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-relay.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/relay --timeout=240s
```

## Verify the result

All required fields from the task are set, and the object reaches the final phase shown by the wait command.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-02-02`.

## Common pitfalls

> [!WARNING]
> Check every field name against the task. A field set at the wrong level of the spec is ignored or rejected, and the grader reads the live object.
