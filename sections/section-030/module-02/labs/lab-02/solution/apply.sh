#!/usr/bin/env bash
set -euo pipefail
current_context="$(kubectl config current-context)"
if [[ "$current_context" != "kind-astro-ats-062-lab-030-02-02" && "$current_context" != "kind-astro-test-ats-062-lab-030-02-02" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
kubectl apply -f "$solution_directory/analysis-probe-args.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Successful analysisrun/manual-run --timeout=240s
