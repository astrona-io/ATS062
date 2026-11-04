---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Compare Two Versions With An Experiment Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-03-01" || exit 1
```

An Experiment creates one ReplicaSet for each template, waits for the duration and then scales the ReplicaSets down.

Save the Experiment with its two templates.

Save this as `experiment-compare-versions.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Experiment
metadata:
  name: compare-versions
  namespace: starfleet
spec:
  duration: 30s
  templates:
  - name: baseline
    replicas: 1
    selector:
      matchLabels:
        app: baseline
    template:
      metadata:
        labels:
          app: baseline
      spec:
        containers:
        - name: web
          image: docker.io/library/python:3.13-alpine
          command:
          - python
          - -m
          - http.server
          - '8080'
  - name: candidate
    replicas: 1
    selector:
      matchLabels:
        app: candidate
    template:
      metadata:
        labels:
          app: candidate
      spec:
        containers:
        - name: web
          image: docker.io/library/python:3.13-alpine
          command:
          - python
          - -m
          - http.server
          - '8080'
```

Apply it:

```sh
kubectl apply -f experiment-compare-versions.yaml
```

Then check the result:

```sh
kubectl -n starfleet get experiment compare-versions -o jsonpath='{.status.phase}{"\n"}'
kubectl -n starfleet get replicasets
```

## Verify the result

The grader reads the Experiment spec, its status phase and the ReplicaSets that it owns.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-03-01`.

## Common pitfalls

> [!WARNING]
> The selector labels of the two templates must differ, or the ReplicaSets would select each other's pods. The phase is `Running` until the duration has passed.
