---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Complete A Canary Revision Through Weight And Pause Steps Solution

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-02" || exit 1
node_name="astro-ats-062-lab-020-01-02-control-plane"
worker_name="astro-ats-062-lab-020-01-02-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Rollouts controller is installed in argo-rollouts. A healthy mission Rollout runs revision one; initial-rollout records its current hash. Revision two has not been applied.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

The starting Rollout is healthy at revision one. Apply revision two with a 50 percent weight, a five-second pause and then 100 percent. Verify a different ReplicaSet becomes stable with two updated ready replicas. This baseline controls replica weights and has no traffic-routing provider; it does not promise exact HTTP request percentages. Preserve initial-rollout, which records the starting hash.

Save this as `rollout-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mission
  template:
    metadata:
      labels:
        app: mission
      annotations:
        lab.example.io/revision: two
    spec:
      containers:
      - name: mission
        image: docker.io/library/python:3.13-alpine
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary:
      steps:
      - setWeight: 50
      - pause:
          duration: 5s
      - setWeight: 100
```

Apply the scoped correction:

```sh
kubectl apply -f rollout-mission.yaml
```

## Verify The Result

Observe the actual result. A denied request returns a nonzero status when the denial works, so run it separately from a shell sequence that stops on error. Status convergence and a successful request establish different parts of the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
sleep 35
```

Advance a real Rollout from revision one to revision two. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.

After recording your result, remove the independent lab with `astrona destroy ats-062-lab-020-01-02`.

## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
