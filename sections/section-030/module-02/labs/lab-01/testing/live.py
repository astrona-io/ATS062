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

t=obj('analysistemplate','probe-gate')
assert 'job' in t['spec']['metrics'][0]['provider'] and any(a['name']=='status' for a in t['spec'].get('args',[])), 'probe-gate must use a job provider and an arg named status'
r=obj('rollout','mission'); st=r['status']
steps=r['spec']['strategy']['canary'].get('steps',[])
assert any('analysis' in x and x['analysis']['templates'][0]['templateName']=='probe-gate' for x in steps), 'An inline analysis step with probe-gate is required'
env={e['name']:e.get('value') for e in r['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'Revision two must be applied'
assert observed(r) and st.get('phase')=='Healthy' and st.get('stableRS')==st.get('currentPodHash'), 'Rollout must be Healthy with the new ReplicaSet stable'
assert st['currentPodHash']!=obj('configmap','initial-rollout')['data']['hash'], 'The initial revision was never replaced'
runs=[x for x in items('analysisruns') if owned_by(x,'Rollout','mission')]
assert runs and any(x['status'].get('phase')=='Successful' for x in runs), 'The Rollout must have created a Successful AnalysisRun'
