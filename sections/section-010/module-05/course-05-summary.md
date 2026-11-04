---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Summary

The Argo Rollouts controller embeds the Argo notifications engine. The engine checks the triggers that a `Rollout` subscribes to on each reconcile and sends messages through a service. No extra pod is needed.

The configuration has four parts. Services define destinations, templates define message bodies, triggers define conditions, and subscriptions are annotations on the `Rollout`. The first three are keys in the ConfigMap `argo-rollouts-notification-configmap`, and credentials are keys in the Secret `argo-rollouts-notification-secret`, both in the namespace of the controller.

A trigger is a list of rules with a `when` condition, an optional `oncePer` expression and a `send` list. A subscription annotation has the form `notifications.argoproj.io/subscribe.<trigger>.<service>`, and its value is the recipient. The engine records what it sent in the annotation `notified.notifications.argoproj.io`.

When no message arrives, check the path from the end: the receiver, the controller log, the annotation names, the trigger condition and the template.

Key facts:

- The ConfigMap and the Secret live in the controller namespace.
- A value that starts with `$` reads a key of the Secret.
- `oncePer` limits a trigger to one message for each value.
- The webhook body must be valid JSON after replacement.

<!-- astrona:playground:destroy -->
