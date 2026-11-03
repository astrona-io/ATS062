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

r=obj('rollout','mission'); st=r['status']
assert observed(r), 'Rollout generation has not been observed'
assert r['spec'].get('revisionHistoryLimit')==3, 'revisionHistoryLimit must be 3'
assert st.get('phase')=='Healthy' and st.get('readyReplicas')==2 and st.get('updatedReplicas')==2, 'Rollout must be Healthy with two updated ready replicas'
sets=[x for x in items('replicasets') if owned_by(x,'Rollout','mission')]
assert sets, 'The controller has not created a ReplicaSet owned by the Rollout'
current=[x for x in sets if x['metadata']['labels'].get('rollouts-pod-template-hash')==st['currentPodHash']]
assert current and current[0]['status'].get('readyReplicas')==2, 'The current ReplicaSet must have two ready pods'
assert 'mission' not in [x['metadata']['name'] for x in items('deployments')], 'No Deployment named mission may exist'
