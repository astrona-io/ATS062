---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Testing And Troubleshooting

A notification setup has many parts, and a failure in any one of them looks the same: no message arrives. This part builds the full setup in the playground, releases a revision, and then shows how to find the broken part when nothing is received.

## Building the setup

Save this as `configmap-notifications.yaml`. It holds the service, the template and the trigger from the earlier parts:

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

<!-- astrona:playground:renew -->

Apply it. The controller reads the configuration; if a change does not seem to apply, restart the controller Deployment:

```sh
kubectl apply -f configmap-notifications.yaml
```

Then save the `Rollout` with the subscription annotation and revision `two`.

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

Apply it, and wait until the release is healthy:

```sh
kubectl apply -f rollout-mission.yaml
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
```

## Reading the result

The `probe` Service stores the JSON bodies that it receives. Read them from the `shuttle` pod:

```sh
kubectl -n starfleet exec shuttle -- python -c 'import urllib.request; print(urllib.request.urlopen("http://probe:8080/hooks").read().decode())'
kubectl -n starfleet get rollout mission -o jsonpath='{.metadata.annotations}{"\n"}'
```

The first command prints a JSON list with one entry for each message that reached the receiver. The second shows the `notified.notifications.argoproj.io` annotation that the engine added.

## Finding the broken part

Work through the path of a message from the end to the start.

1. **Did the receiver get a request?** Read the receiver, as above. If it has the message, the engine works.
2. **Did the engine try?** Read the controller log and look for lines about notifications and the name of the `Rollout`:

```sh
kubectl -n argo-rollouts logs deployment/argo-rollouts --tail=300 | grep -i notif
```

3. **Is the annotation correct?** The trigger and the service names in the annotation must match the ConfigMap keys exactly.
4. **Is the trigger true?** Compare the condition with the real `status.phase`.
5. **Is the template valid?** A template error appears in the log.

The plugin has a command that sends a test message from a template to a service, which helps to test credentials without a release. It is not available in the playground.

## What you know now

A complete setup is a ConfigMap, optional Secret keys and one annotation. A receiver, the controller log and the annotation `notified.notifications.argoproj.io` show where a message stopped. The module closes with the main points.

## Common pitfalls

> [!WARNING]
> The `oncePer` record prevents a second message for the same revision, so a test that reuses the same revision sends nothing the second time. Use a new revision for each test.
