---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Try A Metric In Dry Run

The `starfleet` team wants to try a new metric on an analysis without letting it fail the run.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-01-02" || exit 1
```

## Required result

- Create an AnalysisTemplate named `probe-dry` in `starfleet` with two Job metrics, `stable-check` (the Job exits 0) and `experimental-check` (the Job exits 1), each with `count: 1`.
- In the template, list `experimental-.*` under `dryRun` and set `measurementRetention` to a `limit` of 5 for `.*`.
- Create an AnalysisRun named `dry-run-check` with the same two metrics and the same `dryRun` entry.
- Wait until the AnalysisRun is `Successful`.

## Constraints

- Do not create a Rollout.
- Do not use the web or prometheus providers.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
