---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Guided Practice: Execute A Job Based Analysis

Use a host shell with the private kubeconfig for this module playground. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-030-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-030-01" || exit 1
node_name="astro-ats-062-playground-030-01-control-plane"
worker_name="astro-ats-062-playground-030-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Rollouts controller is installed in argo-rollouts. No learner Rollout or AnalysisRun exists.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

Create the reusable AnalysisTemplate and a run with the same metric. Job success is the metric result; a template alone does not execute an analysis. This exercise runs analysis independently rather than wiring a rollout gate.

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
                - import urllib.request; text=urllib.request.urlopen("http://probe:8080/",timeout=4).read().decode();
                  assert "probe-ready" in text
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
                - import urllib.request; text=urllib.request.urlopen("http://probe:8080/",timeout=4).read().decode();
                  assert "probe-ready" in text
```

Apply the scoped correction:

```sh
kubectl apply -f analysistemplate-probe-check.yaml
```

## Verify The Result

Observe the actual result. A denied request returns a nonzero status when the denial works, so run it separately from a shell sequence that stops on error. Status convergence and a successful request establish different parts of the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/mission-analysis --timeout=240s
```

Complete an AnalysisRun from a real service-health Job. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.


## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
