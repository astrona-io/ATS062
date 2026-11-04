#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-062-lab-020-03-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
manifest_path="$(mktemp)"
curl --fail --silent --show-error --location --max-time 120 'https://github.com/argoproj/argo-rollouts/releases/download/v1.10.0/install.yaml' -o "$manifest_path"
python3 - "$manifest_path" <<'CHECKSUM'
import hashlib,sys
assert hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest() == 'ca8a1785391026023627c8a12db5422e227d7a7a6ec7c01f99f7d5b1726ed53c', 'Controller manifest checksum differs'
CHECKSUM
kubectl apply --server-side -n argo-rollouts -f "$manifest_path"
rm -f "$manifest_path"
kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=300s
kubectl apply -f "$lab_directory/bootstrap/manifests/start.yaml"
kubectl -n starfleet rollout status deployment/probe --timeout=180s
kubectl -n starfleet wait --for=condition=Ready pod/shuttle --timeout=120s
kubectl -n outpost wait --for=condition=Ready pod/drifter --timeout=120s
kubectl apply -f "$lab_directory/bootstrap/manifests/lab-start.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Healthy rollout/mission --timeout=240s
hash="$(kubectl -n starfleet get rollout mission -o jsonpath='{.status.currentPodHash}')"
kubectl -n starfleet create configmap initial-rollout --from-literal=hash="$hash" --dry-run=client -o yaml | kubectl apply -f -
