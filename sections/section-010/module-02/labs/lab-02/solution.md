---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Set A Progress Deadline With Automatic Abort Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-02-02" || exit 1
```

With `progressDeadlineAbort: true`, the controller aborts the release when no progress happens for the whole deadline, instead of only reporting `ProgressDeadlineExceeded`.

Save this as `rollout-beacon.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: beacon
  namespace: starfleet
spec:
  replicas: 2
  progressDeadlineSeconds: 90
  progressDeadlineAbort: true
  selector:
    matchLabels:
      app: beacon
  template:
    metadata:
      labels:
        app: beacon
    spec:
      containers:
      - name: beacon
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
      steps:
      - setWeight: 50
      - pause: {duration: 5s}
```

Apply it:

```sh
kubectl apply -f rollout-beacon.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/beacon --timeout=240s
```

## Verify the result

All required fields from the task are set, and the object reaches the final phase shown by the wait command.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-02-02`.

## Common pitfalls

> [!WARNING]
> Check every field name against the task. A field set at the wrong level of the spec is ignored or rejected, and the grader reads the live object.
