---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Guided Practice: Controller Options

This exercise changes the log level and the log format of the controller and reads the new arguments.

Select the private kubeconfig for this playground:

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-playground-010-03)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-playground-010-03" || exit 1
```

Save the patch that adds the two options to the container arguments.

Save this as `controller-args.yaml`:

```yaml
spec:
  template:
    spec:
      containers:
      - name: argo-rollouts
        args:
        - --loglevel
        - debug
        - --logformat
        - json
```

Apply it:

```sh
kubectl -n argo-rollouts patch deployment argo-rollouts --patch-file controller-args.yaml
```

Then check the result:

```sh
kubectl -n argo-rollouts rollout status deployment/argo-rollouts
kubectl -n argo-rollouts logs deployment/argo-rollouts --tail=5
```

## Common pitfalls

> [!WARNING]
> A debug log is large. Remove the options again when the investigation ends.
