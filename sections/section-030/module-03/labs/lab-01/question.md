---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Compare Two Versions With An Experiment

Before any release, the team wants to run a baseline and a candidate version side by side for a short time.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. No Experiment exists.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-030-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-030-03-01" || exit 1
```

## Required result

- Create an Experiment `compare-versions` in `starfleet` with `duration: 30s` and two templates, `baseline` and `candidate`, each with one replica and the image `docker.io/library/python:3.13-alpine` running `python -m http.server 8080`. Use the labels `app: baseline` and `app: candidate`.
- End state: the Experiment is in phase `Successful` and owns a ReplicaSet for each template.

## Constraints

- Do not create the ReplicaSets yourself; the Experiment creates them.
- Do not change the Rollout `mission`.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
