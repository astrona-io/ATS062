---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Other Providers And The Plugin Route

NGINX and Istio are two of several supported providers. A team may run a cloud load balancer, a mesh with another API, or the Kubernetes Gateway API. This part lists the other options, what they edit, and how a plugin extends the list.

## The built-in providers

Each provider has its own key under `trafficRouting`, and each one edits the object of its own system.

| Provider | Key | What the controller edits |
| --- | --- | --- |
| AWS Application Load Balancer | `alb` | A forward action in the annotations of the Ingress |
| Service Mesh Interface | `smi` | The weights of a `TrafficSplit` |
| Traefik | `traefik` | The weights of a `TraefikService` |
| Ambassador | `ambassador` | Canary `Mapping` objects |
| Apache APISIX | `apisix` | The weights of an `ApisixRoute` |

The ALB integration needs the AWS Load Balancer Controller, which reads the Ingress annotations. SMI is a specification for mesh traffic splits, and a mesh that implements it applies the `TrafficSplit`. The details of each provider are in its own section of the project documentation, and the exam asks for the idea, not every field.

## Combining providers

The `trafficRouting` block accepts more than one provider in the same Rollout. This is used when a mesh handles traffic inside the cluster and an Ingress handles traffic from outside. The controller then sets the same weight in each provider.

## The plugin route and the Gateway API

The Kubernetes Gateway API is a newer standard for traffic routing, with objects such as `HTTPRoute`. The Rollouts controller does not edit these objects itself. It uses a traffic router plugin: a separate executable that the controller starts and calls over a local connection. The plugin is registered in the ConfigMap `argo-rollouts-config` under `trafficRouterPlugins`, with a name and a location of the binary. A Rollout then uses it through `trafficRouting.plugins`, with the plugin name as key and the plugin settings below it. For the Gateway API, the settings name the `HTTPRoute` and its namespace.

Check where the controller reads its plugin settings:

<!-- astrona:playground:renew -->

```sh
kubectl -n argo-rollouts get configmap argo-rollouts-config -o yaml
kubectl explain rollout.spec.strategy.canary.trafficRouting.plugins
```

The first command prints the controller ConfigMap, which has no plugin entries in the playground. The second prints the field description.

## Choosing a provider

Use the provider that already carries your traffic. A cluster with the NGINX Ingress controller uses `nginx`. A cluster with Istio uses `istio`, preferably when header routing or mirroring is needed. A cluster that moves to the Gateway API uses the plugin. The Rollouts controller never installs the provider.

## What you know now

Every provider follows the same contract of two Services and a written weight. The built-in providers cover Ingress controllers and meshes, and a plugin covers the Gateway API and other new systems. The module closes with its main points.

## Common pitfalls

> [!WARNING]
> Feature support differs between providers. A step such as `setHeaderRoute` or `setMirrorRoute` is accepted by the CRD for any provider, but the provider may not implement it, and the Rollout then reports an error. Check the provider before you write the steps.
