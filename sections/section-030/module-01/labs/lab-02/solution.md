---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Try A Metric In Dry Run Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-01-02" || exit 1
```

The metric `experimental-check` fails, but the dry run records the failure and ignores it when the controller decides the phase of the run.

Save this as `analysis-dry-run.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: probe-dry
  namespace: starfleet
spec:
  dryRun:
  - metricName: experimental-.*
  measurementRetention:
  - metricName: .*
    limit: 5
  metrics:
  - name: stable-check
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
                command: ["python", "-c", "print(1)"]
  - name: experimental-check
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
                command: ["python", "-c", "raise SystemExit(1)"]
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisRun
metadata:
  name: dry-run-check
  namespace: starfleet
spec:
  dryRun:
  - metricName: experimental-.*
  metrics:
  - name: stable-check
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
                command: ["python", "-c", "print(1)"]
  - name: experimental-check
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
                command: ["python", "-c", "raise SystemExit(1)"]
```

Apply it:

```sh
kubectl apply -f analysis-dry-run.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/dry-run-check --timeout=240s
```

## Verify the result

All required fields from the task are set, and the object reaches the final phase shown by the wait command.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-01-02`.

## Common pitfalls

> [!WARNING]
> Check every field name against the task. A field set at the wrong level of the spec is ignored or rejected, and the grader reads the live object.
