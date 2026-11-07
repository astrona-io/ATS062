#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-062-capstone-020" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
kubectl apply -f "$solution_directory/rollout-scout.yaml"
kubectl apply -f "$solution_directory/rollout-mission.yaml"
sleep 15
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/scout --timeout=300s
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=300s
