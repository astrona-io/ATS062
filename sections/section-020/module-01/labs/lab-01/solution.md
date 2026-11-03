---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Hold A Blue-Green Revision In Preview Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-01" || exit 1
```

Write the new Rollout spec. The Services stay as they are. The Rollout changes `blueGreen` and the pod template together, so one apply starts the new revision under the new settings.

Save this as `rollout-scout.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: scout
  namespace: starfleet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: scout
  template:
    metadata:
      labels:
        app: scout
    spec:
      containers:
      - name: scout
        image: docker.io/library/python:3.13-alpine
        env:
        - name: REVISION
          value: two
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    blueGreen:
      activeService: scout-active
      previewService: scout-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 60
```

Apply it:

```sh
kubectl apply -f rollout-scout.yaml
```

Then wait for the pause and compare the two Services. The controller writes the `rollouts-pod-template-hash` selector into each one.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Paused rollout/scout --timeout=240s
kubectl -n starfleet get service scout-active -o jsonpath='{.spec.selector}'
kubectl -n starfleet get service scout-preview -o jsonpath='{.spec.selector}'
kubectl -n starfleet get rollout scout -o jsonpath='{.status.stableRS} {.status.currentPodHash}'
```

## Verify the result

The Rollout phase is `Paused`. `status.stableRS` differs from `status.currentPodHash`. The active Service selects `stableRS` and the preview Service selects `currentPodHash`.

When you are done, remove the environment with `astrona destroy ats-062-lab-020-01-01`.

## Common pitfalls

> [!WARNING]
> If `autoPromotionEnabled` stays `true`, the Rollout switches `scout-active` to revision two after the new pods are ready, and the grader sees phase `Healthy`, not `Paused`.
