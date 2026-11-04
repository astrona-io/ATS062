---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Use Common Progressive Rollout Strategies

This section covers the two strategies of a Rollout. Blue-green runs two full sets of pods and moves all traffic at promotion. A canary moves traffic in steps, with weights and pauses, and can use a traffic router for exact weights.

## Modules

1. Blue-Green Deployments
2. Canary Deployments
3. Traffic Management Providers

Each module has a short landing page, up to four parts and a summary. A playground and a graded lab follow the parts. The section ends with a capstone lab and a knowledge check.

## Learning Outcomes

- Explain activeService, previewService and the promotion settings of a blue-green release.
- Write canary steps with setWeight and pause and predict the replica counts.
- Explain trafficRouting, stableService and canaryService.
- Choose a strategy for a given workload.
- Explain how the controller drives a traffic provider, and configure the NGINX Ingress and Istio providers.
- Name the other supported traffic routers and the plugin route.
