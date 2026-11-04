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

t=obj('analysistemplate','web-gate'); m=t['spec']['metrics'][0]
assert 'web' in m['provider'] and 'jsonPath' in m['provider']['web'], 'web-gate must use a web provider with a jsonPath'
assert 'result == 200' in m.get('successCondition',''), 'The success condition must compare result with 200'
r=obj('rollout','mission'); st=r['status']
steps=r['spec']['strategy']['canary'].get('steps',[])
assert any('analysis' in x and x['analysis']['templates'][0]['templateName']=='web-gate' for x in steps), 'An inline analysis step with web-gate is required'
assert env_of(r).get('REVISION')=='two', 'Revision two must be applied'
healthy_new_revision()
runs=[x for x in items('analysisruns') if owned_by(x,'Rollout','mission')]
assert runs and any(x['status'].get('phase')=='Successful' for x in runs), 'The Rollout must have created a Successful AnalysisRun'
