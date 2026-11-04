---
draft: true
exam_objectives:
- Use Common Progressive Rollout Strategies
---
# Summary

A traffic management provider makes a canary weight exact. The Rollouts controller needs a `stableService` and a `canaryService`, edits their selectors with the pod template hashes, and writes the weight into a provider object. The provider controller and the proxy split the requests. The Rollouts controller never sees a request.

With NGINX Ingress, the controller creates a canary Ingress next to the stable Ingress. The Ingress carries the annotations `canary` and `canary-weight`, and extra annotations such as `canary-by-header` come from `additionalIngressAnnotations`. With Istio, the controller edits the weights of a `VirtualService`, either between two Services or between two subsets of a `DestinationRule`.

The other built-in providers are the AWS Application Load Balancer, the Service Mesh Interface, Traefik, Ambassador and Apache APISIX. The Kubernetes Gateway API works through a traffic router plugin that is registered in the controller ConfigMap. A Rollout can use more than one provider at once.

A missing provider controller does not stop a release, so the weights in the status are not proof of the real traffic split. Feature support, such as header and mirror routes, differs by provider.

Key facts:

- The canary Ingress is named `<rollout>-<stable ingress>-canary`.
- `additionalIngressAnnotations` keys are written without the NGINX prefix.
- Istio needs exactly two destinations on a managed route.
- Plugins are registered under `trafficRouterPlugins` in `argo-rollouts-config`.

<!-- astrona:playground:destroy -->
