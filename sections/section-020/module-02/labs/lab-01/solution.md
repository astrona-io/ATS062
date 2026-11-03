---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Complete A Canary Revision With Weight And Pause Steps Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-02-01" || exit 1
```

Write the new spec. The steps run in order: 50 percent of the replicas, a 5 second timed pause, then all of them.

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

Then wait for the end of the steps and read the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get rollout mission -o jsonpath='{.status.stableRS} {.status.currentPodHash} {.status.currentStepIndex}'
kubectl -n starfleet get replicasets -l app=mission
```

## Verify the result

The Rollout is `Healthy`. `status.stableRS` equals `status.currentPodHash` and differs from the hash stored in `initial-rollout`. The annotation `rollout.argoproj.io/revision` is `2`.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-02-01`.

## Common pitfalls

> [!WARNING]
> A `pause` without `duration` stops the Rollout until someone promotes it, and the grader then never sees `Healthy`.
