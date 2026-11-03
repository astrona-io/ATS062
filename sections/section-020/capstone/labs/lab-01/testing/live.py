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

r=obj('rollout','scout'); st=r['status']; bg=r['spec']['strategy']['blueGreen']
assert bg.get('activeService')=='scout-active' and bg.get('previewService')=='scout-preview', 'activeService and previewService are wrong'
assert bg.get('autoPromotionEnabled') is False, 'autoPromotionEnabled must be false'
env={e['name']:e.get('value') for e in r['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'Revision two must be applied'
assert observed(r) and st.get('phase')=='Paused', 'Revision two must wait in preview (phase Paused)'
assert st.get('stableRS') and st['stableRS']!=st.get('currentPodHash'), 'The stable ReplicaSet must still be revision one'
active=obj('service','scout-active'); preview=obj('service','scout-preview')
assert active['spec']['selector'].get('rollouts-pod-template-hash')==st['stableRS'], 'Active Service must select the stable ReplicaSet'
assert preview['spec']['selector'].get('rollouts-pod-template-hash')==st['currentPodHash'], 'Preview Service must select the new ReplicaSet'

m=obj('rollout','mission'); st=m['status']
steps=m['spec']['strategy']['canary'].get('steps',[])
assert len(steps)==3 and steps[0].get('setWeight')==50 and steps[2].get('setWeight')==100, 'The canary steps are wrong'
assert str(steps[1].get('pause',{}).get('duration')) in ('5s','5'), 'The pause duration is wrong'
env={e['name']:e.get('value') for e in m['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'Revision two must be applied'
assert observed(m) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2 and st.get('updatedReplicas')==2, 'Rollout must be Healthy'
assert st['currentPodHash']!=obj('configmap','initial-mission')['data']['hash'], 'The initial revision was never replaced'
assert st.get('stableRS')==st['currentPodHash'], 'The new ReplicaSet must be stable'
assert m['metadata']['annotations'].get('rollout.argoproj.io/revision')=='2', 'Revision 2 must be current'
