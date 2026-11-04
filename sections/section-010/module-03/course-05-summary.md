---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Summary

The Argo Rollouts installation is one manifest. It registers five custom resource definitions, runs one controller Deployment in the `argo-rollouts` namespace, grants the controller access through a ClusterRole, and adds a metrics Service and the configuration objects. The CRDs make the API accept a `Rollout`, and the controller does the work. Without the controller, a `Rollout` is stored but never gets a ReplicaSet or a status.

The controller changes behaviour through command-line arguments. The log level and log format help with troubleshooting. The `--namespaced` option and the namespace-scoped manifest limit its reach, and `--instance-id` lets several controllers share one cluster without managing the same `Rollout`.

The `kubectl argo rollouts` plugin reads releases as a tree and wraps promote, abort, retry, restart, undo and set image. Each command edits fields of the `Rollout`, so `kubectl` can do the same work. The dashboard is a local web view of the same data.

An upgrade applies the new manifest, and running releases continue because their state is in the `Rollout` objects. Removal starts with the workloads and ends with the CRDs, because deleting a CRD deletes every object of its kind.

Key facts:

- The five kinds are Rollout, AnalysisTemplate, ClusterAnalysisTemplate, AnalysisRun and Experiment.
- The controller metrics port is 8090.
- The dashboard listens on port 3100 by default.
- `--instance-id` limits a controller to Rollouts with the matching label.
- Delete the CRDs last.

<!-- astrona:playground:destroy -->
