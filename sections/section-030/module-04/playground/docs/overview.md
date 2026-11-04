---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Guided Practice: The Web Provider

This exercise measures a canary with a `web` provider and reads the AnalysisRun.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-030-04)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-030-04" || exit 1
```

Save the template with the web provider.

Save this as `analysistemplate-web-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: web-gate
  namespace: starfleet
spec:
  metrics:
  - name: probe-status
    count: 1
    failureLimit: 0
    successCondition: result == 200
    provider:
      web:
        url: http://probe.starfleet.svc.cluster.local:8080/work?status=200
        jsonPath: "{$.status}"
        timeoutSeconds: 5
```

Apply it:

```sh
kubectl apply -f analysistemplate-web-gate.yaml
```

Save the Rollout with the analysis step and revision two.

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
          - templateName: web-gate
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the result:

```sh
kubectl -n starfleet get analysisruns
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase}{"\n"}'
```

## Common pitfalls

> [!WARNING]
> The request leaves from the controller pod, so use the full Service name with the namespace.
