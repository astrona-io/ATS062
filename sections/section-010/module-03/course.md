---
draft: true
exam_objectives:
- Understand Argo Rollouts Fundamentals
---
# Installing Argo Rollouts And Using The Plugin

Before a cluster can run a `Rollout`, someone must install the controller and its custom resource definitions. This module explains what the installation contains, how the controller is configured, how the `kubectl argo rollouts` plugin and the dashboard are used, and how the controller is upgraded and removed.

## Learning Goals

- List the objects that the installation manifest creates and say what each one does.
- Choose between the cluster-wide and the namespace-scoped installation.
- Set controller options such as the log level and the instance identifier.
- Name the plugin commands that read and control a release, and the `kubectl` commands that do the same work.
- Describe how to upgrade and how to remove the controller without losing running workloads.

## Before You Start

You need to know what a `Rollout` is and that a controller watches it. The playground has the controller installed. Hands-on steps use `kubectl` only, because the plugin is not installed in the playground.

## Reading Order

1. Installing the controller and the custom resources.
2. Controller options and installation scope.
3. The kubectl plugin.
4. The dashboard, upgrades and removal.
5. Summary.

<!-- astrona:playground -->
