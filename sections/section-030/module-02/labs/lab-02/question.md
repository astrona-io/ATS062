---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Run An AnalysisRun With An Argument

The `starfleet` team wants to test a template by hand before it is used in a release.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. Nothing else exists yet.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-02-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-02-02" || exit 1
```

## Required result

- Create an AnalysisTemplate named `probe-args` in `starfleet` with the argument `service` and one Job metric `probe-up` with `count: 1`. The Job requests `http://{{ args.service }}:8080/` from Python with a 5 second timeout.
- Create an AnalysisRun named `manual-run` from the same metric, with the argument `service` set to `probe`.
- Wait until the AnalysisRun is `Successful`.

## Constraints

- Do not create a Rollout.
- Do not hard-code the Service name in the Job command of the template.
- Do not change the `probe` Service or the `shuttle` pod.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
