---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Complete A Canary Revision Through Weight And Pause Steps

Advance a real Rollout from revision one to revision two.

## Starting state

The Rollouts controller is installed in argo-rollouts. A healthy mission Rollout runs revision one; initial-rollout records its current hash. Revision two has not been applied.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-02" || exit 1
node_name="astro-ats-062-lab-020-01-02-control-plane"
worker_name="astro-ats-062-lab-020-01-02-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

The starting Rollout is healthy at revision one. Apply revision two with a 50 percent weight, a five-second pause and then 100 percent. Verify a different ReplicaSet becomes stable with two updated ready replicas. This baseline controls replica weights and has no traffic-routing provider; it does not promise exact HTTP request percentages. Preserve initial-rollout, which records the starting hash.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
