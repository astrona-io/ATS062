---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Summary

A canary strategy is an ordered list of steps. `setWeight` sets the share of the new version, `pause` with a `duration` waits and continues alone, and `pause: {}` waits for a promotion. The first revision of a Rollout skips the steps. Each later revision starts at step 0, and the new ReplicaSet becomes stable after the last step.

Without a traffic router, the controller turns a weight into a pod count, rounds up, and limits the speed with `maxSurge` and `maxUnavailable` (both default to 1). The real share of requests then follows the pod counts only roughly. With `trafficRouting`, the controller uses `stableService` and `canaryService` and writes exact weights into the router. The router can also route by header or mirror traffic.

A promotion ends a pause, a full promotion skips all remaining steps, an abort returns the weight to 0, and a retry starts the revision again. Canary suits releases whose problems show under real traffic, and blue-green suits workloads that cannot serve two versions at once.

Key facts:

- `maxSurge` and `maxUnavailable` default to 1 and cannot both be 0.
- Weights are replica ratios unless a traffic router is configured.
- `status.currentStepIndex` shows the step that is running.

<!-- astrona:playground:destroy -->
