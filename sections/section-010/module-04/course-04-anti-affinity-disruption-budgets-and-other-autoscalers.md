---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Anti-Affinity, Disruption Budgets And Other Autoscalers

Scaling is only safe when the pods are spread well and when voluntary disruptions cannot remove too many at once. This part covers the scheduling rule that the strategies add, the PodDisruptionBudget and the KEDA autoscaler, which all work with a `Rollout`.

## Anti-affinity between versions

Pod anti-affinity is a scheduling rule that keeps a pod away from nodes that already run pods with certain labels. A blue-green or canary release runs two versions side by side, and a team can want them on different nodes, so a node failure does not remove both. The strategies have an `antiAffinity` field for this.

The field uses one of two forms. `requiredDuringSchedulingIgnoredDuringExecution` is a hard rule: a pod that cannot satisfy it stays `Pending`. `preferredDuringSchedulingIgnoredDuringExecution` is a soft rule with a `weight` from 1 to 100: the scheduler tries to satisfy it. A Rollout using the soft form looks like this:

```yaml
strategy:
  canary:
    antiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        weight: 1
```

<!-- astrona:playground:renew -->

The controller turns the rule into a pod anti-affinity term that uses the label `rollouts-pod-template-hash`. Check the field and its siblings with:

```sh
kubectl explain rollout.spec.strategy.canary.antiAffinity
kubectl explain rollout.spec.strategy.blueGreen.antiAffinity
```

A hard rule on a small cluster is risky. With two nodes, the stable and the canary version can take at most one pod each per node, and the release cannot grow beyond that.

## PodDisruptionBudget

A PodDisruptionBudget (PDB) limits how many pods of a workload a voluntary disruption, such as a node drain, can remove at once. A PDB selects pods by label, so it works with the pods of a `Rollout` like with any pods. The controller does not create PDBs and does not change them.

Save this as `pdb-mission.yaml`:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: mission-pdb
  namespace: starfleet
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: mission
```

Apply it:

```sh
kubectl apply -f pdb-mission.yaml
kubectl -n starfleet get pdb mission-pdb
```

The selector matches the pods of both the stable and the canary ReplicaSet, since both carry `app: mission`. A PDB does not block the controller from scaling down its own ReplicaSets, because that is not an eviction.

## KEDA

KEDA (Kubernetes Event-driven Autoscaling) is a separate project that scales workloads from external events, such as the length of a queue. A `ScaledObject` has a `scaleTargetRef` with `apiVersion`, `kind` and `name`. KEDA uses the scale subresource, so it can target a `Rollout` with `apiVersion: argoproj.io/v1alpha1` and `kind: Rollout`. KEDA creates and manages an HPA for the object, so do not add a second HPA for the same `Rollout`.

## What you know now

Anti-affinity separates versions on nodes, a PDB limits evictions, and KEDA scales a `Rollout` through the same subresource as an HPA. Only one autoscaler should own the count. The module closes with the points to remember.

## Common pitfalls

> [!WARNING]
> A hard anti-affinity rule on a cluster with few nodes can block a release. A PDB with `minAvailable` equal to the replica count blocks node drains completely. Two autoscalers on one `Rollout` write the replica count against each other.
