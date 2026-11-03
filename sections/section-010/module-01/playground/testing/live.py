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
assert r['metadata']['annotations'].get('rollout.argoproj.io/revision')=='2', 'Revision 2 is not current'
assert st.get('phase')=='Healthy' and st.get('stableRS')==st.get('currentPodHash')
sets=[x for x in items('replicasets') if owned_by(x,'Rollout','mission')]
assert len(sets)==2, 'Two ReplicaSets must be owned by the Rollout'
