---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Guided Practice: Rollout Notifications

This exercise builds a webhook notification and reads the message that the receiver stored.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-010-05)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-010-05" || exit 1
```

Save the service, the template and the trigger in the notification ConfigMap.

Save this as `configmap-notifications.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argo-rollouts-notification-configmap
  namespace: argo-rollouts
data:
  service.webhook.probe: |
    url: http://probe.starfleet.svc:8080
    headers:
    - name: Content-Type
      value: application/json
  template.rollout-healthy: |
    webhook:
      probe:
        method: POST
        body: |
          {"rollout": "{{.rollout.metadata.name}}", "revision": "{{.rollout.status.currentPodHash}}"}
  trigger.on-healthy: |
    - when: rollout.status.phase == 'Healthy'
      oncePer: rollout.status.currentPodHash
      send: [rollout-healthy]
```

Apply it:

```sh
kubectl apply -f configmap-notifications.yaml
```

Restart the controller so it reads the new configuration.

Run it:

```sh
kubectl -n argo-rollouts rollout restart deployment/argo-rollouts && kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=240s
```

Save the Rollout with the subscription annotation and revision two.

Save this as `rollout-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: mission
  namespace: starfleet
  annotations:
    notifications.argoproj.io/subscribe.on-healthy.probe: ""
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mission
  template:
    metadata:
      labels:
        app: mission
    spec:
      containers:
      - name: mission
        image: docker.io/library/python:3.13-alpine
        env:
        - name: REVISION
          value: two
        ports:
        - containerPort: 8080
        command:
        - python
        - -m
        - http.server
        - '8080'
  strategy:
    canary: {}
```

Apply it:

```sh
kubectl apply -f rollout-mission.yaml
```

Then check the result:

```sh
kubectl -n starfleet exec shuttle -- python -c 'import urllib.request; print(urllib.request.urlopen("http://probe:8080/hooks").read().decode())'
kubectl -n starfleet get rollout mission -o jsonpath='{.metadata.annotations}{"\n"}'
```

## Common pitfalls

> [!WARNING]
> Use a new revision for each test, because the controller sends only one message for each revision.
