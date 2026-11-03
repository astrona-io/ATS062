---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Summary

The `phase` of a `Rollout` is `Progressing`, `Paused`, `Healthy` or `Degraded`. A pause is a deliberate stop caused by a pause step, a blue-green wait or `spec.paused`. A `Degraded` phase often follows an abort. The controller does not start an aborted revision again until the spec returns to the stable template or an operator retries.

Promote, abort, retry and undo are changes to the `Rollout` object or its status. The `kubectl argo rollouts` plugin wraps them. An undo writes an older pod template back into the spec, so the normal strategy runs again, except inside `rollbackWindow`.

An existing Deployment moves to Argo Rollouts in one of two ways. Converting the object changes its kind and strategy. The field `workloadRef` keeps the Deployment as the source of the pod template, and `scaleDown` decides when the Deployment's own pods stop.

A plain Service only approximates traffic shares through pod counts. A traffic router such as Istio or NGINX Ingress applies exact weights, headers or paths, and the controller edits the router's objects. When Argo CD manages the `Rollout`, Argo CD owns the spec and the controller owns the progress.

The controller records its work in events, in its own log and on its metrics port 8090. A failed release shows as `InvalidSpec`, as `ProgressDeadlineExceeded` or as an abort, and the stable ReplicaSet keeps serving in each case. The way out is a corrected template, an undo, a retry or a restart.

Key facts:

- `workloadRef.scaleDown` accepts `never`, `onsuccess` and `progressively`.
- `stableService` and `canaryService` receive the revision hash selectors when a router is used.
- Replica counts give approximate weights; a router gives exact weights.
- An invalid spec sets the condition `InvalidSpec`.
- `Degraded` does not mean the application is down.

<!-- astrona:playground:destroy -->
