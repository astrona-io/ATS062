---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Block A Bad Release With Background Analysis

The release review needs proof that a failing check stops a canary. Revision two of `mission` is checked against a request that the `probe` Service answers with status 500.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-capstone-030)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-capstone-030" || exit 1
```

## Required result

- Create a ClusterAnalysisTemplate `probe-gate` with two required arguments `status` and `hash` (no defaults) and one metric `probe-ok` (`count: 1`, `failureLimit: 0`) with a `job` provider that requests `http://probe:8080/work?status={{ args.status }}` and fails on an HTTP error.
- Update the Rollout `mission` with background analysis (`strategy.canary.analysis`) that uses `probe-gate` with `clusterScope: true`, the argument `status` set to `"500"` and the argument `hash` taken from `valueFrom.podTemplateHashValue: Latest`. Use the steps `setWeight: 50`, `pause` for `30s`, `setWeight: 100`. Release `REVISION=two`.
- End state: the AnalysisRun created by the Rollout is `Failed` and carries the hash of the new ReplicaSet in its `hash` argument, the Rollout is aborted (`status.abort` is `true`), and the stable ReplicaSet is still revision one.

## Constraints

- Update the existing Rollout.
- Do not create or edit AnalysisRuns by hand.
- Do not change `initial-rollout`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
