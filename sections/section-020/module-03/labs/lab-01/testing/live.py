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

r=obj('rollout','mission'); st=r['status']
c=r['spec']['strategy']['canary']
assert c.get('stableService')=='mission-stable' and c.get('canaryService')=='mission-canary', 'stableService and canaryService are required'
nx=c.get('trafficRouting',{}).get('nginx',{})
assert nx.get('stableIngress')=='mission-ingress', 'trafficRouting.nginx.stableIngress must be mission-ingress'
assert env_of(r).get('REVISION')=='two', 'Revision two must be applied'
assert observed(r) and st.get('phase')=='Paused' and st.get('currentStepIndex')==1, 'The Rollout must be paused at the pause step'
i=obj('ingress','mission-mission-ingress-canary'); a=i['metadata'].get('annotations',{})
assert owned_by(i,'Rollout','mission'), 'The canary Ingress must be owned by the Rollout'
assert a.get('nginx.ingress.kubernetes.io/canary')=='true' and a.get('nginx.ingress.kubernetes.io/canary-weight')=='20', 'The canary Ingress must carry canary true and weight 20'
assert a.get('nginx.ingress.kubernetes.io/canary-by-header')=='X-Canary', 'The header annotation X-Canary is missing'
