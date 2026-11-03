---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Guided Practice: Analysis Step In A Canary

This exercise adds an analysis step to a canary and reads the AnalysisRun that the Rollout creates.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-030-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-030-02" || exit 1
```

Save the template with a `status` argument.

Save this as `analysistemplate-probe-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-gate
  namespace: starfleet
spec:
  args:
  - name: status
    value: "200"
  metrics:
  - name: probe-ok
    count: 1
    failureLimit: 0
    provider:
      job:
        spec:
          backoffLimit: 0
          template:
            spec:
              restartPolicy: Never
              containers:
              - name: check
                image: docker.io/library/python:3.13-alpine
                command:
                - python
                - -c
                args:
                - import urllib.request; urllib.request.urlopen("http://probe:8080/work?status={{ args.status }}", timeout=4)
```

Apply it:

```sh
kubectl apply -f analysistemplate-probe-gate.yaml
```

Then save the second revision with an inline analysis step.

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
      - analysis:
          templates:
          - templateName: probe-gate
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then follow the run. The run name contains the Rollout name, the pod hash and the step index.

```sh
kubectl -n starfleet get analysisruns
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get analysisruns -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
```

## Common pitfalls

> [!WARNING]
> The Job in the metric runs in the namespace of the Rollout and needs network access to the Service it checks.
