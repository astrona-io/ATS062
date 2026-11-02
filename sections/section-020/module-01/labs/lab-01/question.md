---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Separate Blue Green Active And Preview Services

Create active and preview Services managed by a blue-green Rollout.

## Starting state

The Rollouts controller is installed in argo-rollouts. No learner Rollout or AnalysisRun exists.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-01" || exit 1
node_name="astro-ats-062-lab-020-01-01-control-plane"
worker_name="astro-ats-062-lab-020-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

Use activeService active and previewService preview. The controller must add its pod-template-hash selector to the active service. This task grades initial controller reconciliation; it does not claim to exercise a timed manual promotion.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
