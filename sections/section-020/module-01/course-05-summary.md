---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Summary

A blue-green `Rollout` uses an `activeService` that users reach and an optional `previewService` for the new version. The controller adds a `rollouts-pod-template-hash` selector to each Service. A promotion changes the selector of the active Service to the hash of the new ReplicaSet, so no pod restarts and the switch applies to new connections.

The first revision of a `Rollout` becomes active at once. From the second revision on, `autoPromotionEnabled`, `autoPromotionSeconds` and `previewReplicaCount` decide when the switch happens and how much capacity the waiting version uses. The old ReplicaSet runs on for `scaleDownDelaySeconds` (30 seconds by default), so that late connections and a quick rollback still work.

`prePromotionAnalysis` runs before the switch and blocks it when the analysis fails. `postPromotionAnalysis` runs after the switch, and a failure sends the traffic back to the old ReplicaSet. An abort before promotion leaves users on the old version, because the active Service never moved.

A blue-green release switches traffic by writing the hash of a ReplicaSet into the selector of the active Service. `previewReplicaCount` lowers the cost of the preview, a promotion scales up before it switches, and `scaleDownDelaySeconds` keeps the old pods for a delay. A rollback is fast while the old ReplicaSet still runs.

Key facts:

- `autoPromotionEnabled` defaults to `true`; `scaleDownDelaySeconds` defaults to 30.
- Blue-green needs capacity for two full sets of pods.
- A paused blue-green release shows the pause reason `BlueGreenPause`.
- The controller manages the `rollouts-pod-template-hash` entry of the Service selectors.
- `autoPromotionSeconds` promotes by itself after a wait.

<!-- astrona:playground:destroy -->
