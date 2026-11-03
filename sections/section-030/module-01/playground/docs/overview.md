---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Guided Practice: AnalysisTemplate And A Job Metric

This exercise defines a Job-based metric, runs it once as an AnalysisRun, and reads the measurement.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-030-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-030-01" || exit 1
```

Save the template and a run that uses the same metric definition.

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
  name: play-analysis
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

Then read the result. `metricResults` lists each metric with its counters and measurements.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/play-analysis --timeout=240s
kubectl -n starfleet get analysisrun play-analysis -o jsonpath='{.status.phase}'
kubectl -n starfleet get analysisrun play-analysis -o jsonpath='{.status.metricResults}'
kubectl -n starfleet get jobs
```

## Common pitfalls

> [!WARNING]
> The run copies the metric at creation time. Editing the AnalysisTemplate later does not change a run that already exists.
