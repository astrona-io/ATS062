---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Promotion, Analysis Hooks And Rollback

The new version is running in preview. This part explains what decides when it becomes active, how automatic checks can run before and after the switch, and what the controller does when the release fails or is cancelled.

## Settings that control the switch

Four fields in `strategy.blueGreen` control the timing:

- `autoPromotionEnabled`: when `true` (the default), the controller promotes as soon as the new ReplicaSet is ready. When `false`, the Rollout pauses until someone promotes it.
- `autoPromotionSeconds`: with `autoPromotionEnabled: false`, this is a delay after which the controller promotes by itself. When it is not set, the Rollout waits for a manual promotion without end.
- `previewReplicaCount`: the number of pods of the new ReplicaSet while it waits in preview. It saves capacity, and the controller scales the new ReplicaSet to the full size only at promotion. The default is the full replica count.
- `scaleDownDelaySeconds`: how long the old ReplicaSet keeps running after the switch. The default is 30 seconds.

The delay exists because kube-proxy and other components need time to learn the new Endpoints, and clients may still hold connections to the old pods. If the old pods stopped at once, those clients would see errors. A delay of 30 seconds is a safe default, and a larger value gives a longer window to roll back.

## Promotion in a release

The sequence of one release with `autoPromotionEnabled: false` has five steps. First, the template changes. Second, the controller creates the new ReplicaSet and points the preview Service at it. Third, the new pods become ready, and the phase becomes `Paused`. Fourth, someone promotes (for example with `kubectl argo rollouts promote`), which clears the pause. Fifth, the controller moves the active Service to the new hash, and after `scaleDownDelaySeconds` it scales the old ReplicaSet to 0.

<!-- astrona:playground:renew -->

Read the pause reason and the selectors of a paused blue-green `Rollout`. Replace `<NAME>` with the Rollout name:

```sh
kubectl -n starfleet get rollout <NAME> -o jsonpath='{.status.pauseConditions}{"\n"}'
kubectl -n starfleet get rollout <NAME> -o jsonpath='{.status.blueGreen}{"\n"}'
```

The pause condition has the reason `BlueGreenPause`, and `status.blueGreen` lists the hashes of the active and the preview selector.

## Analysis before and after the switch

A person can approve a promotion, and an AnalysisRun can approve it too. The `blueGreen` strategy has two hooks.

`prePromotionAnalysis` runs after the new ReplicaSet is ready and before the active Service moves. If the analysis succeeds, the controller promotes. If it fails, the controller aborts, and the active Service never moved. `postPromotionAnalysis` runs after the active Service moved. If it fails, the controller aborts and returns to the old ReplicaSet, which is why the old ReplicaSet stays up for `scaleDownDelaySeconds`.

Both fields take `templates` (a list of AnalysisTemplate names) and `args`. A typical pre-promotion check runs a smoke test against the preview Service. The argument can carry the name of the preview Service, so one template works for every application:

```yaml
strategy:
  blueGreen:
    activeService: scout-active
    previewService: scout-preview
    prePromotionAnalysis:
      templates:
      - templateName: smoke-test
      args:
      - name: service-name
        value: scout-preview.starfleet.svc.cluster.local
```

This snippet is a fragment of a `Rollout` spec, not a complete file, so it is not applied here. It needs an AnalysisTemplate named `smoke-test` with an argument `service-name`.

## Abort and rollback

An abort in a blue-green release is simple. The active Service has not moved before the promotion, so users have not seen the new version. The controller scales the new ReplicaSet down after `abortScaleDownDelaySeconds` (default 30 seconds). The phase becomes `Degraded` until the spec returns to the stable template.

After a promotion, a rollback is a new release toward the old template. The old ReplicaSet may still be running if it is inside `scaleDownDelaySeconds`. Then the switch back is as quick as the first switch. After the delay, the old ReplicaSet exists with 0 replicas, and the controller must scale it up first, which takes the time of a normal pod start.

## A worked example of the timing

Take a `Rollout` with `replicas: 3`, `autoPromotionEnabled: false`, `autoPromotionSeconds: 120` and `scaleDownDelaySeconds: 60`. A release then follows this timeline. At time 0 the template changes. The new ReplicaSet reaches 3 ready pods after about 20 seconds, and the phase becomes `Paused`. Nobody promotes, so at 140 seconds (20 plus 120) the controller promotes by itself and moves the active Service. At 200 seconds the old ReplicaSet scales to 0.

During the 120 seconds of waiting, the preview Service reaches the new pods and the active Service reaches the old pods. A tester has two minutes to use the preview Service. If the tester finds a problem, an abort in that window stops the release before any user is affected. This is the practical value of `autoPromotionSeconds`: a bounded review window that still ends without a person.

## Choosing the settings

The settings match the risk of the release. A low-risk internal service can use the default `autoPromotionEnabled: true`, because the controller promotes when the pods are ready and the delay protects connections. A service with a smoke test can keep automatic promotion and add `prePromotionAnalysis`, so the controller promotes only when the test passes. A service with a human review keeps `autoPromotionEnabled: false` and no timer.

Capacity is the second factor. With `previewReplicaCount: 1`, a service of 20 pods runs only 1 new pod during the review and uses far less capacity. The controller scales the new ReplicaSet to 20 only at promotion, so a short period exists in which the new pods start and may not be ready yet. A preview with a small count proves that the new image starts, but it does not prove that the new version handles the full load.

## What the controller records

The controller records its decision in the status of the `Rollout`. While the release waits, `status.blueGreen.previewSelector` holds the hash of the new pods and `status.blueGreen.activeSelector` holds the hash of the stable pods. At promotion, the controller writes the new hash into the active Service selector and `status.stableRS` changes to the new hash. Reading these two fields before and after a promotion shows exactly which pods each Service reaches.

A rollback uses the same mechanism in reverse. The old ReplicaSet is still present for the time set by `scaleDownDelaySeconds`, so an undo to the earlier revision only has to change the Service selector back. After the delay has passed, the old ReplicaSet has 0 pods, and an undo must first start pods and wait until they are ready.

## Reading the release from the outside

Three checks tell you where a blue-green release stands without any plugin. Read the phase with `kubectl -n starfleet get rollout scout -o jsonpath='{.status.phase}'`. Read the two selectors from the two Services with `kubectl -n starfleet get svc -o wide`. Compare the hashes in the selectors with the `rollouts-pod-template-hash` label of the pods. If the active hash equals the stable hash and the preview hash equals the current hash, the release is waiting for promotion.

## Common pitfalls

> [!WARNING]
> `autoPromotionEnabled: false` with no `autoPromotionSeconds` waits for a person without a time limit, and an unattended release stays `Paused`. A blue-green release also needs room for two full sets of pods; `previewReplicaCount` lowers only the cost of the waiting period.
