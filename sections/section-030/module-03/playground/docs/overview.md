---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Guided Practice: A Standalone Experiment

This exercise runs two versions as an Experiment and reads its status.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-030-03)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-030-03" || exit 1
```

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

## Common pitfalls

> [!WARNING]
> The pods exist only while the Experiment runs. After the duration, the ReplicaSets are scaled to zero.
