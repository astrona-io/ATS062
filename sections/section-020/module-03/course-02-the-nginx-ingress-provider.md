---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# The NGINX Ingress Provider

The NGINX Ingress controller is a common way to expose Services over HTTP. It can send a share of requests to a second backend through canary annotations on a second Ingress. This part shows how the Rollouts controller creates and edits that second Ingress.

## How NGINX splits traffic

An Ingress is an object that maps hosts and paths to Services. The NGINX Ingress controller reads Ingresses and configures NGINX. When an Ingress carries the annotation `nginx.ingress.kubernetes.io/canary: "true"`, NGINX treats it as a canary for the Ingress with the same host and path. The annotation `nginx.ingress.kubernetes.io/canary-weight` sets the share of requests, as a number from 0 to 100.

The Rollouts controller uses this. It reads the stable Ingress that the team wrote. It then creates a second Ingress, the canary Ingress, with the same rules but with the canary Service as backend and the canary annotations.

## Configuring the Rollout

The `nginx` block names the stable Ingress. The controller names the canary Ingress `<rollout>-<stable ingress>-canary`. The block `additionalIngressAnnotations` adds more annotations to the canary Ingress; the key is written without the NGINX prefix, and the controller adds `nginx.ingress.kubernetes.io/`.

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
      trafficRouting:
        nginx:
          stableIngress: mission-ingress
      steps:
      - setWeight: 20
      - pause: {}
```

<!-- astrona:playground:renew -->

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the result. The Rollout stops at the open pause, and the controller has created the canary Ingress:

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.currentStepIndex}{"\n"}'
kubectl -n starfleet get ingress
kubectl -n starfleet get ingress mission-mission-ingress-canary -o jsonpath='{.metadata.annotations}{"\n"}'
```

The annotations include `nginx.ingress.kubernetes.io/canary` set to `true` and `nginx.ingress.kubernetes.io/canary-weight` set to `20`. The playground has no NGINX Ingress controller, so the annotations are written but no proxy uses them.

## Header routing with NGINX

NGINX also supports a canary by header with the annotation `canary-by-header`. A request with that header set to `always` goes to the canary, and one set to `never` goes to the stable backend. Add it through `additionalIngressAnnotations`:

```yaml
        nginx:
          stableIngress: mission-ingress
          additionalIngressAnnotations:
            canary-by-header: X-Canary
```

The controller writes `nginx.ingress.kubernetes.io/canary-by-header: X-Canary` on the canary Ingress. NGINX then sends a request with `X-Canary: always` to the canary for any weight.

## After the release

At full promotion, the controller sets the weight back to 0 on the canary Ingress, points the stable Service at the new ReplicaSet and keeps the canary Ingress for the next release. The canary Ingress is owned by the Rollout.

## What you know now

The NGINX integration works through a second Ingress with canary annotations. The controller creates it, sets `canary-weight` and adds extra annotations. NGINX does the splitting. The next question is how Istio does the same.

## Common pitfalls

> [!WARNING]
> The stable Ingress must exist before the Rollout reaches `setWeight`. The weight annotation applies only to requests that match the host and path of the stable Ingress. Weights and ingress classes depend on the NGINX Ingress controller that the cluster runs.
