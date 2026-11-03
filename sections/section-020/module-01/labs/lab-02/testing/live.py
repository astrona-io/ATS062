import json,subprocess

def call(*args):
 r=subprocess.run(list(args),text=True,capture_output=True,timeout=20)
 assert r.returncode==0, 'Observation command failed: '+args[0]
 return r.stdout.strip()
def obj(kind,name,ns='starfleet'):
 return json.loads(call('kubectl',*(['-n',ns] if ns else []),'get',kind,name,'-o','json'))
def items(kind,ns='starfleet'):
 return json.loads(call('kubectl','-n',ns,'get',kind,'-o','json'))['items']
def owned_by(item,kind,name):
 return any(o.get('kind')==kind and o.get('name')==name for o in item['metadata'].get('ownerReferences',[]))
def observed(rollout):
 return str(rollout['status'].get('observedGeneration'))==str(rollout['metadata']['generation'])

r=obj('rollout','relay'); st=r['status']; bg=r['spec']['strategy']['blueGreen']
assert bg.get('activeService')=='relay-active' and bg.get('previewService')=='relay-preview', 'activeService and previewService are wrong'
assert bg.get('previewReplicaCount')==1 and bg.get('scaleDownDelaySeconds')==45, 'previewReplicaCount must be 1 and scaleDownDelaySeconds 45'
assert bg.get('activeMetadata',{}).get('labels',{}).get('role')=='active', 'activeMetadata must set role=active'
assert 'role' not in r['spec']['template']['metadata'].get('labels',{}), 'The label role must not be in the pod template'
assert observed(r) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2, 'Rollout must be Healthy with two ready replicas'
active=obj('service','relay-active')
assert active['spec']['selector'].get('rollouts-pod-template-hash')==st.get('stableRS'), 'relay-active must select the stable ReplicaSet'
assert 'relay' not in [x['metadata']['name'] for x in items('deployments')], 'No Deployment named relay may exist'
