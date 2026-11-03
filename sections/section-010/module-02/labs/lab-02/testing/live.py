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

r=obj('rollout','beacon'); st=r['status']; sp=r['spec']
assert sp.get('progressDeadlineSeconds')==90 and sp.get('progressDeadlineAbort') is True, 'progressDeadlineSeconds must be 90 and progressDeadlineAbort true'
steps=sp['strategy']['canary'].get('steps',[])
assert len(steps)==2 and steps[0].get('setWeight')==50 and str(steps[1].get('pause',{}).get('duration')) in ('5s','5'), 'The canary steps are wrong'
assert not sp.get('paused'), 'spec.paused must not be set'
assert observed(r) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2, 'Rollout must be Healthy with two ready replicas'
assert 'beacon' not in [x['metadata']['name'] for x in items('deployments')], 'No Deployment named beacon may exist'
