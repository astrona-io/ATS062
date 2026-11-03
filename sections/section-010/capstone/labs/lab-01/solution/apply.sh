#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-062-lab-010-cap-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
kubectl apply -f "$solution_directory/rollout-bridge.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/bridge --timeout=240s
kubectl apply -f "$solution_directory/rollout-bridge-two.yaml"
sleep 10
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/bridge --timeout=240s
