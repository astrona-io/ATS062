#!/usr/bin/env bash
set -euo pipefail
current_context="$(kubectl config current-context)"
if [[ "$current_context" != "kind-astro-ats-062-lab-010-05-01" && "$current_context" != "kind-astro-test-ats-062-lab-010-05-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"
initial_hash="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash}')"
kubectl apply -f "$solution_directory/configmap-notifications.yaml"
kubectl -n argo-rollouts rollout restart deployment/argo-rollouts && kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=240s
kubectl apply -f "$solution_directory/rollout-mission.yaml"
# The restarted controller needs a few seconds to win leader election; the old
# status still says Healthy, so wait for the new generation to be observed and
# promoted instead of trusting the first Healthy phase.
settled() {
  local generation observed phase stable current
  generation="$(kubectl -n starfleet get rollout mission -o jsonpath='{.metadata.generation}')"
  observed="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.observedGeneration}')"
  phase="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.phase}')"
  stable="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.stableRS}')"
  current="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash}')"
  [[ "$observed" == "$generation" && "$phase" == "Healthy" && -n "$current" && "$stable" == "$current" && "$current" != "$initial_hash" ]]
}
for _ in $(seq 1 120); do
  if settled; then break; fi
  sleep 2
done
settled
