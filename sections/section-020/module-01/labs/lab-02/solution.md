---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Run A Blue-Green Rollout With A Small Preview Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-02" || exit 1
```

The first revision has no earlier revision to protect, so it becomes active at once and the controller writes its hash into the selector of `lander-active`.

Save this as `bluegreen-lander.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: lander-active
  namespace: starfleet
spec:
  selector:
    app: lander
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: lander-preview
  namespace: starfleet
spec:
  selector:
    app: lander
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: lander
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lander
  template:
    metadata:
      labels:
        app: lander
    spec:
      containers:
      - name: lander
        image: docker.io/library/python:3.13-alpine
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    blueGreen:
      activeService: lander-active
      previewService: lander-preview
      previewReplicaCount: 1
      scaleDownDelaySeconds: 45
      activeMetadata:
        labels:
          role: active
```

Apply it:

```sh
kubectl apply -f bluegreen-lander.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/lander --timeout=240s
```

## Verify the result

All required fields from the task are set, and the object reaches the final phase shown by the wait command.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-01-02`.

## Common pitfalls

> [!WARNING]
> Check every field name against the task. A field set at the wrong level of the spec is ignored or rejected, and the grader reads the live object.
