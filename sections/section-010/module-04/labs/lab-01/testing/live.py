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

h=obj('horizontalpodautoscaler','mission-hpa'); s=h['spec']; ref=s['scaleTargetRef']
assert ref.get('apiVersion')=='argoproj.io/v1alpha1' and ref.get('kind')=='Rollout' and ref.get('name')=='mission', 'The HPA must target the Rollout mission'
assert s.get('minReplicas')==2 and s.get('maxReplicas')==5, 'The HPA must scale between 2 and 5 replicas'
res=s['metrics'][0]['resource']
assert res['name']=='cpu' and res['target'].get('type')=='Utilization' and res['target'].get('averageUtilization')==70, 'The HPA must target 70 percent CPU utilization'
r=healthy_new_revision()
req=r['spec']['template']['spec']['containers'][0].get('resources',{}).get('requests',{})
assert 'cpu' in req, 'The container must request CPU so utilization can be computed'
