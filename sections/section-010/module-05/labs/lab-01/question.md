---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Send A Rollout Notification To A Webhook

The team wants a message every time the `mission` Rollout becomes healthy. The `probe` Service in `starfleet` stores every JSON body that it receives at `/hooks`.

## Starting state

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. The Rollout `mission` (canary, no steps, revision `one`) is healthy. The ConfigMap `initial-rollout` records the hash of revision one. The notification ConfigMap has no service, template or trigger.

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-05-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-05-01" || exit 1
```

## Required result

- In the ConfigMap `argo-rollouts-notification-configmap` (namespace `argo-rollouts`) define the webhook service `probe` (URL `http://probe.starfleet.svc:8080`), a template `rollout-healthy` that POSTs a JSON body with the keys `rollout` and `revision` (the value of `rollout.status.currentPodHash`), and a trigger `on-healthy` that sends the template when `rollout.status.phase == 'Healthy'`, once per `currentPodHash`.
- Subscribe the Rollout `mission` with the annotation `notifications.argoproj.io/subscribe.on-healthy.probe: ""` and release `REVISION=two`.
- End state: the Rollout is `Healthy` and `probe` has received a message with `"rollout": "mission"` for the current revision.

## Constraints

- Update the existing Rollout and ConfigMap.
- Do not post to `/hooks` yourself.

## Verify the result

The grader reads the live cluster: object fields, controller status and the objects the controller created. Wait until the controller has finished before you submit. Do not delete or rename objects that the task does not mention.
