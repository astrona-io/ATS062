---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Execute A Job-Based Analysis Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-01-01" || exit 1
```

Write the template and the run in one file. The template is a reusable definition. The run is the object that executes the metric once.

Save this as `analysistemplate-probe-check.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-check
  namespace: starfleet
spec:
  metrics:
  - name: probe-available
    count: 1
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
                - import urllib.request; text=urllib.request.urlopen("http://probe:8080/", timeout=4).read().decode(); assert "probe-ready" in text
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisRun
metadata:
  name: mission-analysis
  namespace: starfleet
spec:
  metrics:
  - name: probe-available
    count: 1
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
                - import urllib.request; text=urllib.request.urlopen("http://probe:8080/", timeout=4).read().decode(); assert "probe-ready" in text
```

Apply it:

```sh
kubectl apply -f analysistemplate-probe-check.yaml
```

Then wait for the run. The controller creates a Kubernetes Job for the measurement, and the Job result becomes the measurement result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/mission-analysis --timeout=240s
kubectl -n starfleet get analysisrun mission-analysis -o jsonpath='{.status.metricResults}'
kubectl -n starfleet get jobs
```

## Verify the result

The AnalysisRun phase is `Successful`. `status.metricResults[0]` has `successful: 1` and one measurement in phase `Successful`.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-01-01`.

## Common pitfalls

> [!WARNING]
> An AnalysisTemplate alone runs nothing. Nothing executes until an AnalysisRun, or a Rollout that references the template, creates one.
