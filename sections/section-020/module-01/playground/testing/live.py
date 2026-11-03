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

r=obj('rollout','mission'); st=r['status']; bg=r['spec']['strategy']['blueGreen']
assert bg.get('activeService')=='active' and bg.get('previewService')=='preview', 'activeService and previewService are wrong'
assert bg.get('autoPromotionEnabled') is False and bg.get('scaleDownDelaySeconds')==60, 'autoPromotionEnabled must be false and scaleDownDelaySeconds 60'
env={e['name']:e.get('value') for e in r['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'Revision two must be applied'
assert observed(r) and st.get('phase')=='Paused', 'Revision two must wait in preview (phase Paused)'
assert st.get('stableRS') and st['stableRS']!=st.get('currentPodHash'), 'The stable ReplicaSet must still be revision one'
active=obj('service','active'); preview=obj('service','preview')
assert active['spec']['selector'].get('rollouts-pod-template-hash')==st['stableRS'], 'Active Service must select the stable ReplicaSet'
assert preview['spec']['selector'].get('rollouts-pod-template-hash')==st['currentPodHash'], 'Preview Service must select the new ReplicaSet'
