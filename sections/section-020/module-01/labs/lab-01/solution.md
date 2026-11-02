---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Separate Blue Green Active And Preview Services Solution

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-01" || exit 1
node_name="astro-ats-062-lab-020-01-01-control-plane"
worker_name="astro-ats-062-lab-020-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Rollouts controller is installed in argo-rollouts. No learner Rollout or AnalysisRun exists.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

Use activeService active and previewService preview. The controller must add its pod-template-hash selector to the active service. This task grades initial controller reconciliation; it does not claim to exercise a timed manual promotion.

Save this as `service-active.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: active
  namespace: starfleet
spec:
  selector:
    app: mission
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: preview
  namespace: starfleet
spec:
  selector:
    app: mission
  ports:
  - port: 8080
    targetPort: 8080
---
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
    blueGreen:
      activeService: active
      previewService: preview
      autoPromotionEnabled: true
```

Apply the scoped correction:

```sh
kubectl apply -f service-active.yaml
```

## Verify The Result

Observe the actual result. A denied request returns a nonzero status when the denial works, so run it separately from a shell sequence that stops on error. Status convergence and a successful request establish different parts of the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
```

Create active and preview Services managed by a blue-green Rollout. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.

After recording your result, remove the independent lab with `astrona destroy ats-062-lab-020-01-01`.

## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
