---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Hold A Blue-Green Revision In Preview

The `scout` Rollout switches to a new revision as soon as it is ready. The team wants to inspect each new revision through a preview Service before any user reaches it.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `scout` (blue-green, revision `one`) is healthy. The Services `scout-active` and `scout-preview` exist.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-020-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-020-01-01" || exit 1
```

## Required result

- Change the Rollout `scout` so `previewService` is `scout-preview`, `autoPromotionEnabled` is `false` and `scaleDownDelaySeconds` is `60`.
- Release revision two by setting the environment variable `REVISION` to `two` in the pod template.
- End state: revision two waits in preview and the Rollout is `Paused`. `scout-active` still selects revision one and `scout-preview` selects revision two.

## Constraints

- Update the existing Rollout; do not delete it.
- Do not promote revision two.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
