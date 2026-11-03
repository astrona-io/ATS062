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

r=obj('rollout','relay'); st=r['status']; sp=r['spec']
assert sp.get('minReadySeconds')==5 and sp.get('progressDeadlineSeconds')==120 and sp.get('revisionHistoryLimit')==2, 'The timing fields are wrong'
assert sp['strategy']['canary'].get('stableMetadata',{}).get('labels',{}).get('role')=='stable', 'stableMetadata must set role=stable'
assert 'role' not in sp['template']['metadata'].get('labels',{}), 'The label role must not be in the pod template'
assert observed(r) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2, 'Rollout must be Healthy with two ready replicas'
pods=[p for p in items('pods') if p['metadata'].get('labels',{}).get('app')=='relay' and p['metadata']['labels'].get('role')=='stable']
assert len(pods)==2, 'Two pods must carry the label role=stable'
assert 'relay' not in [x['metadata']['name'] for x in items('deployments')], 'No Deployment named relay may exist'
