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

d=obj('deployment','argo-rollouts','argo-rollouts')
c=[x for x in d['spec']['template']['spec']['containers'] if x['name']=='argo-rollouts'][0]
args=c.get('args',[])
def option(name):
 for i,a in enumerate(args):
  if a==name and i+1<len(args): return args[i+1]
  if a.startswith(name+'='): return a.split('=',1)[1]
assert option('--loglevel')=='debug', 'The controller must run with --loglevel debug'
assert option('--logformat')=='json', 'The controller must run with --logformat json'
s=d['status']; n=d['spec'].get('replicas',1)
assert s.get('observedGeneration',0)>=d['metadata']['generation'] and s.get('updatedReplicas')==n and s.get('availableReplicas')==n and s.get('replicas')==n, 'The controller Deployment has not finished its rollout'
