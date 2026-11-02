---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Execute A Job Based Analysis

Complete an AnalysisRun from a real service-health Job.

## Starting state

The Rollouts controller is installed in argo-rollouts. No learner Rollout or AnalysisRun exists.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-01-01" || exit 1
node_name="astro-ats-062-lab-030-01-01-control-plane"
worker_name="astro-ats-062-lab-030-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

Create the reusable AnalysisTemplate and a run with the same metric. Job success is the metric result; a template alone does not execute an analysis. This exercise runs analysis independently rather than wiring a rollout gate.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
