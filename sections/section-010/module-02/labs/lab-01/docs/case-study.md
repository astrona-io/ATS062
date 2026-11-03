---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Starting Environment

The Argo Rollouts controller runs in the `argo-rollouts` namespace. The `starfleet` namespace holds the `probe` Service, which answers HTTP requests on port 8080, and the `shuttle` pod. A Deployment named `cargo` (2 replicas, label `app: cargo`) and a Service named `cargo` already exist and are ready.
