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

r=obj('rollout','relay'); st=r['status']; c=r['spec']['strategy']['canary']
assert r['spec'].get('replicas')==4, 'The Rollout must have 4 replicas'
assert c.get('maxSurge')==1 and c.get('maxUnavailable')==0, 'maxSurge must be 1 and maxUnavailable 0'
steps=c.get('steps',[])
assert len(steps)==3 and steps[0].get('setWeight')==50 and steps[2].get('setWeight')==100 and str(steps[1].get('pause',{}).get('duration')) in ('5s','5'), 'The canary steps are wrong'
assert 'trafficRouting' not in c, 'trafficRouting must not be used'
assert observed(r) and st.get('phase')=='Healthy' and st.get('readyReplicas')==4, 'Rollout must be Healthy with four ready replicas'
