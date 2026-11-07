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

t=obj('clusteranalysistemplate','probe-gate',None)
assert 'job' in t['spec']['metrics'][0]['provider'], 'probe-gate must use a job provider'
a=[x for x in t['spec'].get('args',[]) if x['name']=='status']
assert a and 'value' not in a[0], 'The status argument must have no default value'
h=[x for x in t['spec'].get('args',[]) if x['name']=='hash']
assert h and 'value' not in h[0], 'The hash argument must exist and have no default value'
r=obj('rollout','mission'); st=r['status']
bgnd=r['spec']['strategy']['canary'].get('analysis',{})
assert bgnd.get('templates',[{}])[0].get('templateName')=='probe-gate' and bgnd['templates'][0].get('clusterScope') is True, 'Background analysis must use the cluster template'
assert any(x.get('name')=='status' and str(x.get('value'))=='500' for x in bgnd.get('args',[])), 'The status argument must be 500'
assert any(x.get('name')=='hash' and x.get('valueFrom',{}).get('podTemplateHashValue')=='Latest' for x in bgnd.get('args',[])), 'The hash argument must come from podTemplateHashValue Latest'
env={e['name']:e.get('value') for e in r['spec']['template']['spec']['containers'][0].get('env',[])}
assert env.get('REVISION')=='two', 'Revision two must be applied'
assert st.get('abort') is True, 'The Rollout must be aborted'
assert st.get('stableRS')==obj('configmap','initial-rollout')['data']['hash'], 'The stable ReplicaSet must still be revision one'
runs=[x for x in items('analysisruns') if owned_by(x,'Rollout','mission')]
failed=[x for x in runs if x['status'].get('phase')=='Failed']
assert failed, 'The Rollout must own a Failed AnalysisRun'
assert any(any(a.get('name')=='hash' and a.get('value')==st.get('currentPodHash') for a in x['spec'].get('args',[])) for x in failed), 'The Failed run must carry the hash of the new ReplicaSet'
