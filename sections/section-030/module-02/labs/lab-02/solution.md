---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Run A Job-Based Analysis With An Argument Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-02" || exit 1
```

Write the template and the run in one file. The template is a reusable definition, and nothing runs until an AnalysisRun exists. The argument `service` has no default, so the run must set it. The controller replaces `{{ args.service }}` in the Job command with `probe` before it creates the Job.

Save this as `analysis-probe-args.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-args
  namespace: starfleet
spec:
  args:
  - name: service
  metrics:
  - name: probe-up
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
                - "import urllib.request; text=urllib.request.urlopen('http://{{ args.service }}:8080/', timeout=5).read().decode(); assert 'probe-ready' in text"
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisRun
metadata:
  name: manual-run
  namespace: starfleet
spec:
  args:
  - name: service
    value: probe
  metrics:
  - name: probe-up
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
                - "import urllib.request; text=urllib.request.urlopen('http://{{ args.service }}:8080/', timeout=5).read().decode(); assert 'probe-ready' in text"
```

Apply it:

```sh
kubectl apply -f analysis-probe-args.yaml
```

Then wait for the run. The controller creates a Kubernetes Job for the measurement, and the Job result becomes the measurement result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/manual-run --timeout=240s
kubectl -n starfleet get analysisrun manual-run -o jsonpath='{.status.metricResults}'
kubectl -n starfleet get jobs
```

## Verify the result

The AnalysisRun phase is `Successful`. `status.metricResults[0]` is named `probe-up`, has `successful: 1` and one measurement in phase `Successful`. The template keeps `{{ args.service }}` in its Job command.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-02-02`.

## Common pitfalls

> [!WARNING]
> An AnalysisTemplate alone runs nothing. Nothing executes until an AnalysisRun, or a Rollout that references the template, creates one. A run made by hand has no template to supply argument values, so an argument without a `value` in the run ends it in `Error`.
