---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Notifications

A team that releases often wants to learn about a release without watching a terminal. The Argo Rollouts controller can send a message when a release starts, pauses, fails or completes. This module explains how the notification engine is configured, how a `Rollout` subscribes to events, and how to test and debug the setup.

## Learning Goals

- Name the three kinds of configuration: services, templates and triggers.
- Write a webhook service, a template and a trigger in the notification ConfigMap.
- Subscribe a `Rollout` to a trigger with an annotation.
- Find out why a notification was not sent.

## Before You Start

You need to know the phases of a `Rollout`. The playground has the controller, a healthy `Rollout` named `mission` and the `probe` Service. The `probe` Service records every JSON body that it receives with a POST request, so it plays the role of the receiver.

## Reading Order

1. How the notification engine works.
2. Services and templates.
3. Triggers and subscriptions.
4. Testing and troubleshooting.
5. Summary.

<!-- astrona:playground -->
