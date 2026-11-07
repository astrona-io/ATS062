---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Run A Job-Based Analysis With An Argument

Before the next release the `starfleet` team wants a reusable health check for the `probe` Service, written as a template that takes the Service name as an argument, and proof that the check passes now.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080 with a body that contains `probe-ready`, and the `shuttle` pod. No AnalysisTemplate and no AnalysisRun exist.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-02" || exit 1
```

## Required result

- Create an AnalysisTemplate named `probe-args` in `starfleet` with the argument `service` (no default value) and one `job` metric `probe-up` with `count: 1`. The Job pod runs `python -c` with a script that requests `http://{{ args.service }}:8080/` with a 5 second timeout and asserts that the body contains `probe-ready`.
- Create an AnalysisRun named `manual-run` by hand, with the same metric and the argument `service` set to `probe`.
- Wait until the AnalysisRun is `Successful` with one successful measurement.

## Constraints

- The Job needs `backoffLimit: 0` and `restartPolicy: Never`.
- Do not create a Rollout.
- Do not hard-code the Service name in the Job command of the template.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
