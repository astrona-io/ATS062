---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Traffic Routing, Controlling A Canary And Choosing A Strategy

Replica counts only approximate a weight. This part shows how a traffic router makes the weight exact, how to control a canary that is in progress, and how to decide between a canary and a blue-green release.

## Exact weights with trafficRouting

The field `strategy.canary.trafficRouting` tells the controller to use a traffic router. The Rollout then needs two Services: `stableService` and `canaryService`. The controller adds the `rollouts-pod-template-hash` selector to each, so `stableService` reaches the stable pods and `canaryService` reaches the canary pods.

With a router, `setWeight` no longer depends on pod counts. The controller writes the weight into the routing object, for example an Istio `VirtualService` or an NGINX Ingress annotation, and the router splits the requests. The canary can run 1 pod and still receive 50 percent of the requests, because the router counts requests, not pods.

This also changes the scale. Without a router, the canary's pod count follows the weight. With a router, the controller by default keeps the canary at full size during the steps unless `setCanaryScale` is used. `dynamicStableScale: true` makes the stable ReplicaSet shrink as the weight moves away from it, which saves capacity.

A router also enables header-based and mirror steps. With `setHeaderRoute`, requests that carry a given header go to the canary, so testers can reach the new version while other users stay on the stable one. With `setMirrorRoute`, a copy of the requests goes to the canary and the answers are ignored.

<!-- astrona:playground:renew -->

To see the fields that the CRD accepts under `trafficRouting`:

```sh
kubectl explain rollout.spec.strategy.canary.trafficRouting
```

## Controlling a canary in progress

The controls are the same as for any release. A promotion ends the current pause and runs the next step. A full promotion (`promote --full`) skips all remaining steps and analysis and goes to 100 percent. An abort moves the weight back to 0 and scales the canary down after `abortScaleDownDelaySeconds` (default 30). A retry runs an aborted revision again from step 0.

Two details help in practice. A timed pause continues alone, so promotion only matters for open-ended pauses. And a change of the pod template during a canary starts a new release at step 0. The new revision becomes the canary, and the controller does not finish the earlier one.

## Canary or blue-green

The two strategies suit different needs. The table below compares them on the points that matter in an exam question.

| Point | Canary | Blue-green |
| --- | --- | --- |
| Capacity during release | Grows by `maxSurge` | Two full sets of pods |
| Traffic to new version | Gradual, in steps | All at once at promotion |
| Exact weights | Only with a traffic router | Not applicable |
| Testing before users | With header routes and a router | Preview Service |
| Rollback | Weight returns to 0 | Service selector returns |
| Mixed versions for users | Yes, during the steps | No |

Choose a canary when a bug might appear only under real traffic, because the share of affected users stays small. Choose blue-green when the application cannot serve two versions at once, for example when the two versions need different database schemas, or when you want a full test on a preview before anyone is switched.

## Which Services the controller edits

With `trafficRouting`, the controller edits the selectors of `stableService` and `canaryService`. It adds `rollouts-pod-template-hash` to each selector, with the hash of the stable ReplicaSet for `stableService` and the hash of the canary ReplicaSet for `canaryService`. Both Services must exist before the Rollout, and their selectors must match the labels in the pod template. The controller does not create them.

Without `trafficRouting`, a single Service that selects `app` reaches all pods of both ReplicaSets, and the split follows the pod counts. This is why a canary without a router is called a replica-based canary.

## Supported routers

The controller supports several routers through the `trafficRouting` block. Each has its own key under it, for example `istio`, `nginx`, `alb`, `smi`, `traefik`, `ambassador` and `apisix`. A router is a separate component that must already be installed in the cluster. The controller does not install it. It only changes the routing object that belongs to the router, for example the weights of an Istio `VirtualService` or the canary annotations of a second NGINX Ingress.

Every router supports `setWeight`. Header routes and mirror routes work only on routers that implement them, so a Rollout that uses `setHeaderRoute` must run on a router that supports it. The CRD accepts the field with any router, and an unsupported combination is reported as an error in the Rollout status.

## Reading the result of a step

During a canary, three fields show the progress. `status.currentStepIndex` is the index of the step that runs now. `status.canary.weights.canary.weight` holds the weight that the controller wrote to the router, when a router is used. `status.pauseConditions` lists the reason for a pause, for example `CanaryPauseStep`. Reading these three fields tells you whether a release waits for time, waits for a person, or progresses.

## Capacity during a canary

Capacity is a practical limit. A replica-based canary with 10 replicas and `maxSurge: 25%` may run up to 13 pods during the update, because 25 percent of 10 rounds up to 3. A canary with a router and the default full-size canary may need close to twice the pods, because the canary ReplicaSet is scaled to the full count while the stable ReplicaSet is still running. Setting `setCanaryScale` to a small replica count, or setting `dynamicStableScale: true`, lowers this peak. Plan for the peak when you set resource quotas on the namespace, because a quota that is too small leaves new pods in a pending state and the release stalls.

## When a step does not finish

A release that stops moving has one of three causes. The pause has no duration and waits for a promotion. The new pods are not ready, so the ReplicaSet never reaches the count that the step needs. Or the Rollout is past `progressDeadlineSeconds`, and the phase is `Degraded`. Read `status.phase`, `status.pauseConditions` and the conditions in `status.conditions` to tell which one applies. The conditions carry a reason and a message in plain text.

## Releasing a second revision and watching it

Use the Rollout from the previous part. Change the `REVISION` value in `rollout-canary.yaml` from `one` to `two` and apply the file again:

```sh
kubectl apply -f rollout-canary.yaml
```

The controller starts a new release at step 0. Read the progress with:

```sh
kubectl -n starfleet get rollout canary-demo -o jsonpath='{.status.phase} {.status.currentStepIndex}{"\n"}'
kubectl -n starfleet get rs -l app=canary-demo
```

After the 30-second pause the release reaches the open-ended pause. The phase is then `Paused`, and the two ReplicaSets have 2 pods each. To continue without the plugin, clear the pause with a patch on the status:

```sh
kubectl -n starfleet patch rollout canary-demo --subresource=status --type=merge -p '{"status":{"pauseConditions":null}}'
```

This is the same change that a promotion makes. The controller then runs the next step, which sets the weight to 100 percent.

## Common pitfalls

> [!WARNING]
> A canary without a router has no exact weights. A pause with no `duration` blocks the release until someone promotes it. A second template change in the middle of a canary starts over at step 0 for the newest revision.
