---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Traffic Management Providers

A canary without a traffic router can only approximate a weight with pod counts. A traffic management provider is a component in the cluster that splits requests by exact weight. This module explains how the controller drives a provider, how the NGINX Ingress and Istio integrations work, and what the other providers need.

## Learning Goals

- Describe what the controller changes in a provider and what the provider changes in the traffic.
- Configure the NGINX Ingress integration and read the canary Ingress that the controller creates.
- Describe the two ways to use Istio: two Services or one Service with subsets.
- Name the other supported providers and the plugin route for the Gateway API.

## Before You Start

You need to know canary steps, `setWeight` and the roles of `stableService` and `canaryService`. The playground has the controller, two Services and an Ingress for the `mission` Rollout. It has no Ingress controller and no service mesh, so it shows the objects the controller writes, not real traffic.

## Reading Order

1. How the controller drives a provider.
2. The NGINX Ingress provider.
3. The Istio provider.
4. Other providers and the plugin route.
5. Summary.

<!-- astrona:playground -->
