---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Gate A Canary Step With An AnalysisRun Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-01" || exit 1
```

Write the template first. The `{{ args.status }}` placeholder is replaced by the argument value when a run starts.

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

Then update the Rollout. The `analysis` step makes the controller create an AnalysisRun and wait for its result before the next step.

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

Then check the Rollout and its runs.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
kubectl -n starfleet get analysisruns
kubectl -n starfleet get rollout mission -o jsonpath='{.status.stableRS} {.status.currentPodHash}'
```

## Verify the result

The Rollout is `Healthy` and `stableRS` equals `currentPodHash`. `kubectl -n starfleet get analysisruns` lists a run named after the Rollout with phase `Successful`.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-02-01`.

## Common pitfalls

> [!WARNING]
> Apply the template before the Rollout. If the Rollout references a missing template, it reports an error and does not reach the analysis step.
