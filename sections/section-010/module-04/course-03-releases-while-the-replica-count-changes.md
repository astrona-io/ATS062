---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Releases While The Replica Count Changes

Autoscaling and releases happen at the same time in a real cluster. A traffic peak can start a scale-up while a canary is at 20 percent. This part explains how the controller divides a changing count between versions for the canary and blue-green strategies.

## Canary without a traffic router

Without a router, a canary weight is turned into a number of pods. The controller takes the weight as a percentage of `spec.replicas`, rounds up, and keeps the stable ReplicaSet at the remaining size within the limits of `maxSurge` and `maxUnavailable`. With 10 replicas and a weight of 20, the canary has 2 pods and the stable ReplicaSet has 8.

If the HPA raises the count to 20 during the pause, the controller recalculates on the next reconcile. The canary then has 4 pods and the stable ReplicaSet has 16. The weight stays at 20 percent, and the number of pods follows the count. The same happens when the count falls.

## Canary with a traffic router

With a traffic router, the weight is a share of requests, not of pods. By default the controller keeps the canary at the full size of `spec.replicas` during the steps, so the canary can serve its share. With `setCanaryScale`, the canary size is set by a step and does not follow the count unless the step uses `weight`. With `dynamicStableScale: true`, the stable ReplicaSet shrinks as the weight moves to the canary.

## Blue-green

A blue-green Rollout runs two full sets. The active set has `spec.replicas` pods. The preview set has `previewReplicaCount` pods if that field is set, and otherwise `spec.replicas`. After promotion, the old set stays for `scaleDownDelaySeconds` (default 30) and then scales down. An HPA that raises `spec.replicas` raises the size of the set that the controller scales, so both sets grow until the old one goes away.

## Reading the split in the playground

<!-- astrona:playground:renew -->

The playground `Rollout` has no steps, so a template change replaces the pods by rolling update. Read the ReplicaSet sizes at any time with:

```sh
kubectl -n starfleet get replicasets -l app=mission -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,READY:.status.readyReplicas
kubectl -n starfleet get rollout mission -o jsonpath='{.status.replicas} {.status.updatedReplicas} {.status.availableReplicas}{"\n"}'
```

The first command prints the size of each ReplicaSet. The second prints the totals the controller reports. During a release, `updatedReplicas` counts the pods of the newest revision.

## Limits during a surge

A scale-up during a release adds pods in both versions. The cluster needs room for the surge. If the nodes have no free capacity, new pods stay `Pending`, the release cannot progress and the `progressDeadlineSeconds` timer can run out. Capacity planning for a `Rollout` therefore includes the extra pods of the strategy: `maxSurge` for a canary and a full second set for blue-green.

## What you know now

The count is a total. A canary without a router follows the count in pods, a canary with a router follows it only when the canary is scaled by the step, and blue-green scales the sets it runs. A scale-up during a release needs spare capacity. The next question is how scheduling rules and disruptions affect the pods.

## Common pitfalls

> [!WARNING]
> Rounding up makes a small canary larger than the weight suggests. A weight of 10 on 4 replicas gives 1 pod, which is 25 percent. With an HPA, the share of traffic seen by the canary changes whenever the count changes, so use a traffic router when the exact share matters.
