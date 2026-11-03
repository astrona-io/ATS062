---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Prerequisites

This task runs in its own kind cluster (Kubernetes in Docker). You need `astrona`, `kubectl`, Docker or Podman, and a shell. Argo Rollouts is installed in the `argo-rollouts` namespace when the environment starts.

A kubeconfig file holds the address and credentials that `kubectl` uses. Select the one for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-01-01" || exit 1
```
