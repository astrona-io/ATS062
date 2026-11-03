---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Header Routing And Mirroring

A weight sends a random share of requests to the canary. Sometimes the team needs a different rule: only requests from testers, or a copy of live requests that the canary receives without answering to users. Argo Rollouts supports both with two step types that work through the traffic router. This part explains them and the conditions for using them.

## Routes the controller owns

The controller edits the routes of the traffic router. For header routing and mirroring, the `Rollout` lists the names of the extra routes it may manage in `strategy.canary.trafficRouting.managedRoutes`. Each entry is a `name`. The controller creates the route with that name when a step asks for it and removes it when the step is cleared. Routes that are not in the list are never touched.

## Header-based routing

The step `setHeaderRoute` sends requests that carry a given header to the canary, whatever the weight is. It has a `name` (one of the managed routes) and a `match` list. Each match names a `headerName` and a `headerValue` with one of `exact`, `regex` or `prefix`. A step with `setHeaderRoute` and no `match` removes the route.

Save this as `rollout-header-route.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
spec:
  replicas: 3
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
        managedRoutes:
        - name: tester-route
        - name: mirror-route
        istio:
          virtualService:
            name: mission-vsvc
            routes:
            - primary
      steps:
      - setHeaderRoute:
          name: tester-route
          match:
          - headerName: x-team
            headerValue:
              exact: testers
      - pause: {}
      - setHeaderRoute:
          name: tester-route
      - setWeight: 20
```

The file needs Istio and a `VirtualService` named `mission-vsvc` with a route named `primary`. Apply it only on a cluster that has them. The first step makes requests with `x-team: testers` reach the canary, the pause lets testers work, and the third step removes the route.

## Mirroring

The step `setMirrorRoute` copies live requests to the canary. The user still gets the answer from the stable pods, and the canary answer is dropped. It has a `name`, a `percentage` and an optional `match` list of conditions on `method`, `path` or headers. A step with no `match` and no `percentage` removes the mirror route.

```yaml
      - setMirrorRoute:
          name: mirror-route
          percentage: 20
          match:
          - method:
              exact: GET
```

The snippet is a step to add under `steps`, shown to read. A mirror suits read requests. Mirrored write requests reach the canary and may change data.

## Which routers support them

Header routing and mirroring need support in the provider. Istio supports both. Other providers support some of them, and the support differs between versions. A `Rollout` that uses a step the provider does not support is rejected by the controller as an invalid spec. Check the provider list of the installed version before you use these steps.

Check that the controller accepted a `Rollout` that uses them:

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{range .status.conditions[*]}{.type}={.status}{"\n"}{end}'
```

An `InvalidSpec=True` line means the controller rejected the spec.

## What you know now

A weight chooses requests at random, a header route chooses them by content and a mirror copies them. The controller manages only the routes in `managedRoutes`. The next module moves from deploying to measuring: the analysis resources that decide whether a release continues.

## Common pitfalls

> [!WARNING]
> A `setHeaderRoute` step stays active until a later step removes it, so the final steps must clear the route. A mirror to a canary that writes to a shared database can create duplicate data.
