---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Analysis Capstone: Block A Bad Release With Background Analysis Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-cap-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-cap-01" || exit 1
```

Write the cluster-wide template. A ClusterAnalysisTemplate has no namespace, and the runs created from it run in the namespace of the Rollout.

Save this as `clusteranalysistemplate-probe-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ClusterAnalysisTemplate
metadata:
  name: probe-gate
spec:
  args:
  - name: status
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
kubectl apply -f clusteranalysistemplate-probe-gate.yaml
```

Then update the Rollout with background analysis. Background analysis starts with the update and runs next to the steps.

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
      analysis:
        templates:
        - templateName: probe-gate
          clusterScope: true
        args:
        - name: status
          value: "500"
      steps:
      - setWeight: 50
      - pause:
          duration: 30s
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then wait for the abort and read the evidence.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.abort}'=true rollout/mission --timeout=240s
kubectl -n starfleet get analysisruns -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.stableRS} {.status.currentPodHash}'
```

## Verify the result

`status.abort` is `true`. One AnalysisRun owned by `mission` has phase `Failed`. `status.stableRS` is still the hash stored in `initial-rollout`.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-cap-01`.

## Common pitfalls

> [!WARNING]
> The argument `status` has no default in the cluster template. If the Rollout does not pass it, the AnalysisRun cannot start and the Rollout reports an error instead of a failed analysis.
