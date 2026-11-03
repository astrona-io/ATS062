---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Gate A Canary Step With An AnalysisRun

The `mission` canary must not reach 100 percent until the `probe` Service answers a check request with status 200.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-01" || exit 1
```

## Required result

- Create an AnalysisTemplate `probe-gate` with an argument `status` (default `"200"`) and one metric `probe-ok` (`count: 1`, `failureLimit: 0`) with a `job` provider. The Job requests `http://probe:8080/work?status={{ args.status }}` and fails if the request fails.
- Update the Rollout `mission` with the steps `setWeight: 50`, an inline `analysis` step that uses `probe-gate`, and `setWeight: 100`. Release `REVISION=two`.
- End state: the Rollout is `Healthy`, the new ReplicaSet is stable, and the Rollout owns an AnalysisRun in phase `Successful`.

## Constraints

- Update the existing Rollout.
- Do not create the AnalysisRun yourself; the Rollout creates it.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
