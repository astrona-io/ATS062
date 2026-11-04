import json,subprocess

def call(*args):
 r=subprocess.run(list(args),text=True,capture_output=True,timeout=30)
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
def healthy_new_revision():
 r=obj('rollout','mission'); st=r['status']
 assert observed(r) and st.get('phase')=='Healthy' and st.get('stableRS')==st.get('currentPodHash'), 'Rollout must be Healthy with the newest ReplicaSet stable'
 assert st['currentPodHash']!=obj('configmap','initial-rollout')['data']['hash'], 'The initial revision was never replaced'
 return r
def env_of(rollout):
 return {e['name']:e.get('value') for e in rollout['spec']['template']['spec']['containers'][0].get('env',[])}

e=obj('experiment','compare-versions'); s=e['spec']
assert s.get('duration')=='30s', 'The experiment duration must be 30s'
assert sorted(t['name'] for t in s['templates'])==['baseline','candidate'], 'The experiment needs the templates baseline and candidate'
assert e['status'].get('phase')=='Successful', 'The experiment must finish in phase Successful'
rs=[x for x in items('replicasets') if owned_by(x,'Experiment','compare-versions')]
assert len(rs)>=2, 'The experiment must own a ReplicaSet for each template'
