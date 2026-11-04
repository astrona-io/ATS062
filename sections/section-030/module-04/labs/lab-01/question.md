---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Measure A Canary With A Web Provider

The `mission` canary must not reach 100 percent until the controller itself reads status 200 from the `probe` Service.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-04-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-04-01" || exit 1
```

## Required result

- Create an AnalysisTemplate `web-gate` with one metric `probe-status` (`count: 1`, `failureLimit: 0`, `successCondition: result == 200`) and a `web` provider that requests `http://probe.starfleet.svc.cluster.local:8080/work?status=200` and selects `{$.status}` with `jsonPath`.
- Update the Rollout `mission` with the steps `setWeight: 50`, an inline `analysis` step that uses `web-gate`, and `setWeight: 100`. Release `REVISION=two`.
- End state: the Rollout is `Healthy`, the new ReplicaSet is stable, and the Rollout owns an AnalysisRun in phase `Successful`.

## Constraints

- Update the existing Rollout.
- Do not create the AnalysisRun yourself; the Rollout creates it.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
