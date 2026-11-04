---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# The kubectl Plugin

A `Rollout` has a status with many fields, and promoting or aborting a release means editing that status by hand. The `kubectl argo rollouts` plugin wraps these actions in short commands and prints a readable tree of the release. This part lists the commands, says what each one changes in the cluster, and shows the `kubectl` commands that give the same result when the plugin is missing.

## Installing the plugin

A kubectl plugin is an executable file whose name starts with `kubectl-`. When it is on the `PATH`, `kubectl argo rollouts` runs the file `kubectl-argo-rollouts`. The plugin is a release binary of the project. On macOS the package manager Homebrew installs it with `brew install argoproj/tap/kubectl-argo-rollouts`. On other systems, download the binary for the platform from the project releases, make it executable and move it into a directory on the `PATH`.

The plugin talks to the Kubernetes API with the same kubeconfig as `kubectl`. It does not need the controller to be reachable. The playground does not have the plugin, so the examples below are for reading, and the `kubectl` equivalents are the ones to run.

## Reading commands

These commands only read:

- `kubectl argo rollouts list rollouts` lists the Rollouts of a namespace with their strategy, step and replica counts.
- `kubectl argo rollouts get rollout mission` prints a tree with the Rollout, its ReplicaSets, pods and analysis runs. The flag `--watch` updates the tree while the release runs.
- `kubectl argo rollouts status mission` waits until the release is healthy or degraded and exits with a result code, so a pipeline can use it.
- `kubectl argo rollouts version` prints the plugin version.

The equivalent reads with `kubectl` are:

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get rollouts
kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase} {.status.currentStepIndex}{"\n"}'
kubectl -n starfleet get replicasets,pods -l app=mission
```

The first command lists the Rollouts. The second prints the phase and the current step, and the third lists the objects the controller created.

## Controlling commands

These commands change a release. Each one edits the `Rollout` object, and the controller then acts:

- `promote mission` clears the pause conditions so the next step runs. With `--full`, it skips the remaining steps and analysis.
- `abort mission` sets `status.abort` to true, and the controller returns traffic to the stable ReplicaSet.
- `retry rollout mission` clears the abort so the revision starts again.
- `restart mission` sets `spec.restartAt`, which makes the controller replace pods one by one.
- `undo mission` writes an earlier pod template back into the spec. The flag `--to-revision` selects which one.
- `set image mission mission=<image>` changes the image of a container in the pod template, which creates a new revision.
- `pause mission` sets `spec.paused` to true.

Because these commands edit fields, `kubectl patch` gives the same effect. For a restart, patch the field directly:

```sh
kubectl -n starfleet patch rollout mission --type merge -p '{"spec":{"restartAt":"2030-01-01T00:00:00Z"}}'
```

A time in the past or the present makes the controller restart the pods once. A future time schedules the restart, so use a past time to restart now.

## Other commands

The plugin has commands for work around a release. `create` makes a `Rollout`, an `AnalysisRun` or an `Experiment` from a file. `lint -f rollout.yaml` checks a file for errors without applying it. `dashboard` starts a local web interface. `notifications` helps test notification templates. `completion` prints a shell completion script.

## What you know now

The plugin shows a release as a tree and wraps promote, abort, retry, restart, undo and set image. Each command edits fields of the `Rollout`, so `kubectl get` and `kubectl patch` can replace it. The next question is the graphical view and how the controller is upgraded.

## Common pitfalls

> [!WARNING]
> The plugin version and the controller version should match closely, because the plugin reads status fields that newer controllers may change. A `promote` on a release that is not paused has no effect. The `abort` command does not delete anything; it stops the rollout and keeps the stable ReplicaSet.
