---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Vendor Providers And Plugins

Teams that use a hosted monitoring product need a provider for it. Argo Rollouts has providers for several products and a plugin system for the rest. This part lists the providers, shows how credentials reach them and explains the plugin route.

## The vendor providers

Each provider is a key under `provider`, next to `job`, `web` and `prometheus`.

| Key | System | What the metric holds |
| --- | --- | --- |
| `datadog` | Datadog | A query for the Datadog metrics API |
| `newRelic` | New Relic | An NRQL query |
| `cloudWatch` | Amazon CloudWatch | One or more metric data queries |
| `graphite` | Graphite | A query for the render API |
| `influxdb` | InfluxDB | A Flux query |
| `wavefront` | Wavefront | A query string |
| `skywalking` | Apache SkyWalking | A GraphQL expression |
| `kayenta` | Kayenta | A canary analysis configuration |

All of them return their answer to the controller, and the controller evaluates the same condition fields. They differ in the shape of the answer, so the condition changes.

## Credentials

A vendor provider needs credentials, which the controller reads from a Secret in its own namespace. The Datadog provider reads a Secret named `datadog` with the keys `address`, `api-key` and `app-key`. The New Relic provider reads a Secret named `newrelic` with a personal API key, an account identifier and a region. CloudWatch uses the AWS credentials that the controller pod has, for example through a service account role.

Look at the secrets in the controller namespace. A fresh installation has only the notification Secret. Print names only:

<!-- astrona:playground:renew -->

```sh
kubectl -n argo-rollouts get secrets
kubectl explain analysistemplate.spec.metrics.provider.datadog
```

The first command lists the secrets by name without showing values. The second prints the fields of the Datadog provider.

## An example with Datadog

A Datadog metric sets `interval`, an API `query` and a condition. The answer is a list of numbers, so the condition reads `result[0]`. Newer Datadog providers accept several queries and a formula that combines them.

```yaml
provider:
  datadog:
    interval: 5m
    query: |
      avg:requests.error.rate{service:{{ args.service }}}
```

## Metric provider plugins

A provider that is not built in can be added as a plugin. A metric provider plugin is a separate executable. The controller registers it in the ConfigMap `argo-rollouts-config` under `metricProviderPlugins`, with a `name` and a `location` of the file or an address. A metric then selects the plugin with `provider.plugin`, using the plugin name as the key, and the settings below it are passed to the plugin. The controller starts the plugin and calls it for each measurement.

## What you know now

Vendor providers cover the common monitoring products, and each reads its credentials from a Secret. A plugin adds any other source. The last part explains how to write conditions for these answers.

## Common pitfalls

> [!WARNING]
> A missing or misnamed Secret makes every measurement an error. A plugin location that the controller pod cannot read stops the plugin from starting. Credentials belong in Secrets and arguments, never in the template.
