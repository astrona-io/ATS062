---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Triggers And Subscriptions

A template does nothing until a trigger fires it and a `Rollout` subscribes to the trigger. This part shows how to write a trigger with a condition, how to avoid sending the same message again, and how an annotation connects a `Rollout` to a trigger and a service.

## Triggers

A trigger is a key named `trigger.<name>`. Its value is a list of rules. Each rule has a `when` condition, an optional `oncePer` expression and a `send` list of template names. The condition is an expression over the `Rollout` object, which is available as `rollout`.

```yaml
trigger.on-healthy: |
  - when: rollout.status.phase == 'Healthy'
    oncePer: rollout.status.currentPodHash
    send: [rollout-healthy]
```

The condition is true while the phase is `Healthy`. Without `oncePer`, the engine would send the message again each time the state becomes true after being false. With `oncePer`, the engine sends one message for each distinct value of the expression. Here the value is the pod template hash, so each revision sends one message when it becomes healthy.

Typical conditions use `rollout.status.phase`, for example `'Paused'` or `'Degraded'`, and `rollout.status.abort == true`. A rule can also look at the analysis runs through the status message.

## Subscribing a Rollout

A subscription is an annotation on the `Rollout`. The key has this form: `notifications.argoproj.io/subscribe.<trigger>.<service>`. The value is the recipient, such as a Slack channel name. A webhook has no recipient, so the value is an empty string.

The annotation goes under `metadata.annotations` of the `Rollout`:

```yaml
metadata:
  name: mission
  namespace: starfleet
  annotations:
    notifications.argoproj.io/subscribe.on-healthy.probe: ""
```

The annotation names the trigger `on-healthy` and the service `probe`. Both must exist in the ConfigMap, or nothing is sent. Changing an annotation does not create a revision, because only the pod template defines one.

## Default triggers and the catalog

A cluster can define default subscriptions in the ConfigMap with the key `defaultTriggers` for a service, so every `Rollout` that names only the service gets those triggers. The Argo project also publishes a catalog of ready triggers and templates, for example for a paused, failed or completed rollout. A team can copy entries from the catalog and change them. The setup in this module defines its own entries, so no catalog is needed.

## What the engine remembers

After it sends a message, the engine writes the result into an annotation on the `Rollout`, named `notified.notifications.argoproj.io`. It holds a record of the triggers and the values of `oncePer` that were already sent. This record is how the engine avoids duplicates, and a person who deletes it makes the engine send again.

## What you know now

A trigger is a rule with a condition and templates. `oncePer` limits repeats. The annotation `notifications.argoproj.io/subscribe.<trigger>.<service>` connects a `Rollout` to the trigger and the service. The next question is how to prove that it all works.

## Common pitfalls

> [!WARNING]
> A subscription that names a trigger or a service that does not exist sends nothing, and the failure appears only in the controller log. Without `oncePer`, a condition that flips between true and false sends many messages.
