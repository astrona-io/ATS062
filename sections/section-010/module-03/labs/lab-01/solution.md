---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Configure The Controller Log Level And Format Solution

Select the private kubeconfig for this environment:

```sh
export KUBECONFIG="$(astrona kubeconfig ats-062-lab-010-03-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-062-lab-010-03-01" || exit 1
```

A strategic merge patch merges the container entry by its `name`, so one patch file is enough.

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
kubectl -n argo-rollouts get deployment argo-rollouts -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}'
```

## Verify the result

The grader reads the arguments of the container and checks that the Deployment has finished replacing the controller pod.

When you are done, remove the environment with `astrona destroy ats-062-lab-010-03-01`.

## Common pitfalls

> [!WARNING]
> A patch applied with `kubectl apply` replaces the `args` list of the container, so list every option you want. The controller pod restarts, so wait for the rollout to finish before you submit.
