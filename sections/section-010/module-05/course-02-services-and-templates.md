---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Services And Templates

A message needs a destination and a body. Services define the destination, and templates define the body. This part shows how to write both in the ConfigMap, how to keep credentials in the Secret, and which fields of the `Rollout` a template can use.

## Services

A service is one key in the ConfigMap with the name `service.<type>` or `service.<type>.<name>`. The value is a YAML document with the settings of the service. The generic webhook service has a `url` and optional `headers`. A webhook service called `probe` looks like this:

```yaml
service.webhook.probe: |
  url: http://probe.starfleet.svc:8080
  headers:
  - name: Content-Type
    value: application/json
```

The name `probe` is chosen by the author. A subscription uses it later. Other service types have their own fields. The Slack service has a `token`, and the email service has `host`, `port`, `username`, `password` and `from`.

## Keeping credentials in the Secret

A value that starts with `$` is a reference to a key of the Secret `argo-rollouts-notification-secret`. A Slack service reads its token like this:

```yaml
service.slack: |
  token: $slack-token
```

The key `slack-token` must exist in the Secret. This keeps the token out of the ConfigMap, which many people can read.

## Templates

A template is a key named `template.<name>`. For a webhook, the template names the service and gives the request settings. Templates use Go template syntax with the `Rollout` object in `.rollout`. The expression `{{.rollout.metadata.name}}` is the name of the `Rollout`, and `{{.rollout.status.phase}}` is its phase.

```yaml
template.rollout-healthy: |
  webhook:
    probe:
      method: POST
      body: |
        {"rollout": "{{.rollout.metadata.name}}", "revision": "{{.rollout.status.currentPodHash}}"}
```

The key `probe` under `webhook` is the service name from the first example. The body is a JSON text. The `probe` Service in the playground parses the body as JSON, so it must be valid JSON after the placeholders are replaced.

For chat services, a template has a `message` field and often service-specific blocks, such as Slack attachments. The placeholders work in the same way.

## Fields a template can use

The engine gives a template the full object of the `Rollout`. The useful fields are `metadata.name`, `metadata.namespace`, `status.phase`, `status.message`, `status.currentPodHash`, `status.stableRS`, `status.canary.weights` and the images in `spec.template.spec.containers`.

<!-- astrona:playground:renew -->

Check which fields a live `Rollout` has before you write a placeholder:

```sh
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.currentPodHash}{"\n"}'
```

A placeholder for a field that does not exist is replaced by an empty value or makes the template fail, so test with real objects.

## What you know now

A service holds a destination and a reference to its credentials, and a template holds a message body with placeholders from the `Rollout`. Both are keys in the ConfigMap. The next question is when a message is sent.

## Common pitfalls

> [!WARNING]
> A webhook body that is not valid JSON after replacement makes the receiver reject it. Quote every placeholder inside JSON strings. Never put a token directly in the ConfigMap; use the Secret.
