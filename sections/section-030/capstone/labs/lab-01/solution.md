---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Block A Bad Release With Background Analysis Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-capstone-030)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-capstone-030" || exit 1
```

Write the cluster-wide template. A ClusterAnalysisTemplate has no namespace, and the runs created from it run in the namespace of the Rollout. The template declares two arguments without defaults: `status` for the HTTP status the Job requests, and `hash` for the pod template hash of the revision under test. The Job prints the hash before it sends the request, so the Job log shows which revision was checked.

Save this as `clusteranalysistemplate-probe-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ClusterAnalysisTemplate
metadata:
  name: probe-gate
spec:
  args:
  - name: status
  - name: hash
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
                - import urllib.request; print("checking pod template hash {{ args.hash }}"); urllib.request.urlopen("http://probe:8080/work?status={{ args.status }}", timeout=4)
```

Apply it:

```sh
kubectl apply -f clusteranalysistemplate-probe-gate.yaml
```

Then update the Rollout with background analysis. Background analysis starts with the update and runs next to the steps. The argument `hash` takes its value from `valueFrom.podTemplateHashValue: Latest`, so the controller fills in the hash of the newest ReplicaSet when it creates the run.

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
        - name: hash
          valueFrom:
            podTemplateHashValue: Latest
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
kubectl -n starfleet get analysisruns -o jsonpath='{range .items[*]}{.metadata.name} {.spec.args}{"\n"}{end}'
```

## Verify the result

`status.abort` is `true`. One AnalysisRun owned by `mission` has phase `Failed`. `status.stableRS` is still the hash stored in `initial-rollout`. In the run, the argument `hash` holds the same value as `status.currentPodHash`.

When you are done, remove the environment with `astrona destroy ats-062-capstone-030`.

## Common pitfalls

> [!WARNING]
> The arguments `status` and `hash` have no default in the cluster template. If the Rollout does not pass both, the AnalysisRun cannot start and the Rollout reports an error instead of a failed analysis.
