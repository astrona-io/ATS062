---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Run An AnalysisRun With An Argument Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-02" || exit 1
```

The argument `service` has no default, so the run must set it. The controller replaces `{{ args.service }}` in the Job command with `probe` before it creates the Job.

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
                - "import urllib.request; urllib.request.urlopen('http://{{ args.service }}:8080/', timeout=5)"
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
                - "import urllib.request; urllib.request.urlopen('http://{{ args.service }}:8080/', timeout=5)"
```

Apply it:

```sh
kubectl apply -f analysis-probe-args.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/manual-run --timeout=240s
```

## Verify the result

All required fields from the task are set, and the object reaches the final phase shown by the wait command.

When you are done, remove the environment with `astrona destroy ats-062-lab-030-02-02`.

## Common pitfalls

> [!WARNING]
> Check every field name against the task. A field set at the wrong level of the spec is ignored or rejected, and the grader reads the live object.
