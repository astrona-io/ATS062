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

c=obj('configmap','argo-rollouts-notification-configmap','argo-rollouts')['data']
assert 'service.webhook.probe' in c and 'template.rollout-healthy' in c and 'trigger.on-healthy' in c, 'The ConfigMap needs the service, the template and the trigger'
r=healthy_new_revision()
assert 'notifications.argoproj.io/subscribe.on-healthy.probe' in r['metadata'].get('annotations',{}), 'The Rollout needs the subscription annotation'
out=call('kubectl','-n','starfleet','exec','shuttle','--','python','-c','import urllib.request; print(urllib.request.urlopen("http://probe:8080/hooks").read().decode())')
msgs=json.loads(out)
assert any(m.get('rollout')=='mission' and m.get('revision')==r['status']['currentPodHash'] for m in msgs), 'The receiver did not get a message for the current revision'
