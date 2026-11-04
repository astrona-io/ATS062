---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Summary

The `Rollout` CRD declares the scale subresource. It maps the desired count to `spec.replicas`, the current count to `status.replicas` and the selector to `status.selector`. Because of this, `kubectl scale`, the HorizontalPodAutoscaler and KEDA work with a `Rollout` without special code. A count change is not a revision.

An HPA targets a `Rollout` with `apiVersion: argoproj.io/v1alpha1` and `kind: Rollout`. It needs a metrics server and CPU requests on the containers. The HPA decides how many pods in total, and the controller decides how they are divided between versions. Only one writer should own `spec.replicas`.

During a release, a canary without a traffic router follows the count in pods, rounded up. A canary with a router depends on its scale settings. A blue-green Rollout scales the sets it runs. A scale-up during a release needs spare capacity, or pods stay pending and the progress deadline can pass.

Anti-affinity separates the versions on nodes, soft or hard. A PodDisruptionBudget limits evictions and works on the pod labels. KEDA scales through the same subresource and creates its own HPA.

Key facts:

- `spec.replicas` defaults to 1.
- The HPA `scaleTargetRef` names the Rollout, not the Deployment.
- Utilization needs a CPU request.
- Hard anti-affinity can leave pods pending.
- One autoscaler per Rollout.

<!-- astrona:playground:destroy -->
