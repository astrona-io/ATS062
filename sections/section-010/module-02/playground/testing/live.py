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

r=obj('rollout','crew-rollout'); st=r['status']
ref=r['spec'].get('workloadRef',{})
assert ref.get('kind')=='Deployment' and ref.get('name')=='crew', 'workloadRef must point to the Deployment crew'
assert ref.get('scaleDown')=='onsuccess', 'scaleDown must be onsuccess'
assert 'template' not in r['spec'], 'A Rollout with workloadRef must not define its own template'
assert observed(r) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2, 'Rollout must be Healthy with 2 ready replicas'
assert obj('deployment','crew')['spec'].get('replicas')==0, 'The Deployment must be scaled to zero after success'
ep=obj('endpoints','crew'); n=sum(len(x.get('addresses',[])) for x in ep.get('subsets',[]))
assert n==2, 'Service crew must still have 2 ready endpoints'
