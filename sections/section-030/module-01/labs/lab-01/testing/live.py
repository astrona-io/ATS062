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

t=obj('analysistemplate','probe-dry'); sp=t['spec']
assert any(d.get('metricName')=='experimental-.*' for d in sp.get('dryRun',[])), 'The template must list experimental-.* in dryRun'
assert any(m.get('limit')==5 for m in sp.get('measurementRetention',[])), 'measurementRetention must have a limit of 5'
assert [m['name'] for m in sp['metrics']]==['stable-check','experimental-check'], 'The template must define the two metrics in order'
run=obj('analysisrun','dry-run-check')
assert run['status']['phase']=='Successful', 'The AnalysisRun must be Successful'
names={m['name'] for m in run['status']['metricResults']}
assert names=={'stable-check','experimental-check'}, 'Both metrics must have a result'
