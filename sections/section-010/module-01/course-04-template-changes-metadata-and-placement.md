---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Template Changes, Metadata And Placement

A release starts when the pod template changes. Not every change to a pod is a template change, and not every change that the controller makes to a pod starts a release. This part separates the changes that create a revision from the labels and annotations that the controller adds on its own, and it shows how to keep the pods of two revisions on different nodes.

## What creates a revision

The controller hashes `spec.template`. Any change to the containers, the images, the commands, the environment variables, the volumes or the labels and annotations inside `spec.template.metadata` produces a new hash. A new hash means a new ReplicaSet, a new revision number and a new release that follows the strategy.

Changes outside the template do not produce a new hash. These are `spec.replicas`, `spec.strategy`, `spec.minReadySeconds`, `spec.revisionHistoryLimit`, `spec.paused` and the metadata of the `Rollout` itself. The controller reads them in the next reconcile and applies them to the existing ReplicaSets.

Check the current hash and revision, change only the replica count, and read the values again:

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash} {.metadata.annotations.rollout\.argoproj\.io/revision}{"\n"}'
kubectl -n starfleet patch rollout mission --type merge -p '{"spec":{"replicas":3}}'
kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash} {.metadata.annotations.rollout\.argoproj\.io/revision}{"\n"}'
```

The two lines show the same hash and the same revision number, because the replica count is not part of the template.

## Metadata that does not create a revision

During a release, you often need to tell the pods of the two revisions apart, for example with a label that a monitoring rule or a Service selector uses. A label put in the pod template would change the hash. For this case the strategy has its own metadata fields. The controller adds the labels and annotations to the pods after the ReplicaSet creates them, without changing the template.

For a canary strategy, the fields are `canaryMetadata` and `stableMetadata`. For a blue-green strategy, they are `previewMetadata` and `activeMetadata`. Each field has `labels` and `annotations`. A pod that belongs to the canary ReplicaSet gets the canary metadata. When the release finishes and the pod becomes stable, the controller removes the canary metadata and adds the stable metadata.

Save this as `rollout-metadata.yaml`:

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
      canaryMetadata:
        labels:
          role: canary
      stableMetadata:
        labels:
          role: stable
      steps:
      - setWeight: 50
      - pause: {duration: 10s}
```

Apply it:

```sh
kubectl apply -f rollout-metadata.yaml
```

Then check the result. The pods of the stable ReplicaSet carry the label `role: stable`:

```sh
kubectl -n starfleet get pods -l app=mission --show-labels
```

The labels are on the pods only. The ReplicaSet and the pod template do not hold them, which is why the hash stayed the same.

## Placing the two revisions on different nodes

When both revisions run at the same time, the scheduler may place their pods on the same node. If that node fails, both revisions fail together. The strategy field `antiAffinity` asks the controller to add a pod anti-affinity rule to the new ReplicaSet, so its pods avoid the nodes of the other revision. A canary and a blue-green strategy both accept it.

The field has two forms. `requiredDuringSchedulingIgnoredDuringExecution: {}` is a hard rule: a pod that cannot find a free node stays `Pending`. `preferredDuringSchedulingIgnoredDuringExecution` takes a `weight` between 1 and 100 and is a soft rule: the scheduler tries to follow it and places the pod anyway when it cannot. The controller builds the rule with the label `rollouts-pod-template-hash`, so only the pods of the other revision are avoided.

```yaml
  strategy:
    blueGreen:
      activeService: active
      antiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          weight: 1
```

The snippet belongs under `spec.strategy` of a blue-green `Rollout` and is shown to read, not to apply on its own.

## What you know now

The template hash is the only thing that starts a release, and the metadata fields of the strategy let the controller label pods without changing it. The `antiAffinity` field keeps the two revisions on different nodes when the cluster has enough of them. The next module looks at how an operator reads the state of a release and controls it.

## Common pitfalls

> [!WARNING]
> A label added to `spec.template.metadata` starts a new release, even though the application did not change. Use `canaryMetadata` or `stableMetadata` for labels that only exist to tell revisions apart. A hard `requiredDuringSchedulingIgnoredDuringExecution` rule on a cluster with few nodes leaves the new pods `Pending` and the release stuck.
