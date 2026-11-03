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

r=obj('rollout','bridge'); st=r['status']
assert observed(r), 'Rollout generation has not been observed'
assert r['spec'].get('replicas')==3 and r['spec'].get('revisionHistoryLimit')==2, 'replicas must be 3 and revisionHistoryLimit 2'
assert r['spec']['strategy'].get('canary') is not None and 'blueGreen' not in r['spec']['strategy'], 'canary strategy required'
env={e['name']:e.get('value') for e in r['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'The pod template must carry REVISION=two'
assert r['metadata']['annotations'].get('rollout.argoproj.io/revision')=='2', 'Revision 2 must be current (update the same Rollout)'
assert st.get('phase')=='Healthy' and st.get('readyReplicas')==3 and st.get('stableRS')==st.get('currentPodHash'), 'Rollout must be Healthy and stable'
assert 'bridge' not in [x['metadata']['name'] for x in items('deployments')], 'No Deployment named bridge may exist'
ep=obj('endpoints','bridge'); n=sum(len(x.get('addresses',[])) for x in ep.get('subsets',[]))
assert n==3, 'Service bridge must have 3 ready endpoints'
