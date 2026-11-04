#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-062-lab-010-03-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
kubectl -n argo-rollouts patch deployment argo-rollouts --patch-file "$solution_directory/controller-args.yaml"
kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=240s
