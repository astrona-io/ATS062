---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Rollout Controller, ReplicaSets And Promotion State

Argo Rollouts provides progressive-delivery control through a Rollout resource and its controller. It can coordinate canary or blue-green strategies, pauses and analysis gates. The resource is distinct from a standard Kubernetes Deployment even though both involve workload versions and ReplicaSets.

## Declare A Strategy And Workload Template

A Rollout specifies the application template, replica intent and supported strategy fields. The controller manages relevant ReplicaSets and progression state. Kubernetes still schedules Pods, runs containers and reports readiness. A progressive-delivery resource does not remove image access, capacity or runtime dependencies.

The installed custom resource definitions and controller must support the selected fields. Kubernetes storing an object without a functioning implementation does not provide the intended rollout. Controller status and actual workload relationships are therefore necessary evidence alongside the spec.

## Versions Need Capacity And Readiness

A new template creates a version transition under the strategy. The old stable population and new population can coexist, consuming additional capacity. Resource requests, available nodes and readiness determine whether the new version can serve its intended share.

A ready Pod satisfies the configured readiness contract, not every business validation. An endpoint that returns success for a shallow health check can still produce incorrect results for users. Progressive delivery can use analysis or explicit promotion decisions to add evidence beyond basic readiness.

## Promotion Is A Managed Decision

A strategy can pause or require conditions before shifting traffic or declaring the new version stable. The meaning of a pause, step and promotion depends on the strategy. A manual promotion is an authorized decision, while automated analysis interprets its configured measurements and thresholds.

Neither should be treated as universal proof of safety. Review what was measured, which population supplied the evidence and whether missing data was handled correctly. A low-traffic canary can appear quiet because it received little work rather than because the new version is healthy.

## Routing Integration Has Its Own Contract

Some progressive traffic control relies on supported ingress or service-mesh integration. Services and routing resources must point to the intended stable and canary populations. A desired weight is input to that integration, while observed requests establish the actual distribution under connections, retries and other behavior.

A standard Service without such integration can approximate traffic share through replica counts in some scenarios, but that is not the same as precise request-weight control. Choose the supported mechanism and explain its limitations rather than infer percentages solely from Pod counts.

## Ownership And Recovery Remain Explicit

Argo CD can manage the desired Rollout resource, while the Rollouts controller manages its progression. Their responsibilities should cooperate. Direct edits to Git-owned intent can be restored by later reconciliation. Status and generated child resources should not be mistaken for independent desired-state sources.

Aborting or returning to a stable version does not reverse every database migration, external write or credential change. Recovery must preserve compatibility and assess side effects. A useful rollout design connects desired version, capacity, routing, analysis and recovery so promotion is a justified transition rather than a green label without context.

## Common pitfalls

> [!WARNING]
> Rollout readiness is not complete promotion evidence. Routing weights, actual traffic and external-state recovery have separate contracts, and controller ownership must fit Git-managed intent.
