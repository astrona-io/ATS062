---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Gate A Blue-Green Switch And Set The Canary Scale Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-capstone-020)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-capstone-020" || exit 1
```

Write the blue-green change for `scout`. `prePromotionAnalysis` runs after the new ReplicaSet is ready and before the active Service moves. Automatic promotion stays on, so the controller promotes by itself as soon as the AnalysisRun ends `Successful`.

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
      autoPromotionEnabled: true
      prePromotionAnalysis:
        templates:
        - templateName: probe-gate
        args:
        - name: status
          value: "200"
```

Apply it:

```sh
kubectl apply -f rollout-scout.yaml
```

Then write the canary change for `mission`. `setCanaryScale` and `dynamicStableScale` only work with `trafficRouting`, so the Rollout names the two Services and the stable Ingress. The controller creates the canary Ingress itself and writes the weight into its annotations.

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
    spec:
      containers:
      - name: mission
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
    canary:
      stableService: mission-stable
      canaryService: mission-canary
      dynamicStableScale: true
      trafficRouting:
        nginx:
          stableIngress: mission-ingress
      steps:
      - setCanaryScale:
          replicas: 1
      - setWeight: 50
      - pause:
          duration: 10s
      - setWeight: 100
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then wait for both Rollouts and read the evidence. The AnalysisRun of `scout` needs a Job pod to finish, so the first wait can take a minute or two.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/scout --timeout=300s
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=300s
kubectl -n starfleet get analysisruns -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
kubectl -n starfleet get rollouts
kubectl -n starfleet get ingress
```

## Verify the result

`scout` shows `Healthy`, `stableRS` equals `currentPodHash`, `scout-active` selects that hash, and an AnalysisRun owned by `scout` is `Successful`. `mission` shows `Healthy` with `stableRS` equal to `currentPodHash` and a different hash than `initial-mission`, and the Ingress `mission-mission-ingress-canary` exists with the annotation `nginx.ingress.kubernetes.io/canary: "true"`.

When you are done, remove the environment with `astrona destroy ats-062-capstone-020`.

## Common pitfalls

> [!WARNING]
> A `setCanaryScale` step or `dynamicStableScale: true` without `trafficRouting` is rejected by the controller, and the Rollout reports an invalid spec instead of starting the release. Set the Services and the stable Ingress in the same change as the steps.
