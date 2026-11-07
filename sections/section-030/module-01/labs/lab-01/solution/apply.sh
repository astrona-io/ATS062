#!/usr/bin/env bash
set -euo pipefail
current_context="$(kubectl config current-context)"
if [[ "$current_context" != "kind-astro-ats-062-lab-030-01-01" && "$current_context" != "kind-astro-test-ats-062-lab-030-01-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
kubectl apply -f "$solution_directory/analysis-dry-run.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/dry-run-check --timeout=240s
