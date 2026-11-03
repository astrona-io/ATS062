---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Execute A Job-Based Analysis

Before the next release the team wants a reusable health check for the `probe` Service, and proof that the check passes now.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. No AnalysisTemplate and no AnalysisRun exist.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-01-01" || exit 1
```

## Required result

- Create an AnalysisTemplate `probe-check` in `starfleet` with one metric `probe-available`, `count: 1`, and a `job` provider. The Job pod runs `python -c` with a script that requests `http://probe:8080/` and asserts that the body contains `probe-ready`.
- Create an AnalysisRun `mission-analysis` with the same metric, and wait until its phase is `Successful`.

## Constraints

- The Job needs `backoffLimit: 0` and `restartPolicy: Never`.
- Do not change the `probe` Service.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
