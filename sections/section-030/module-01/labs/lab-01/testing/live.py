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

t=obj('analysistemplate','probe-check')
m=t['spec']['metrics'][0]
assert m['name']=='probe-available' and m.get('count')==1 and 'job' in m['provider'], 'The template must define the job metric probe-available with count 1'
run=obj('analysisrun','mission-analysis'); assert run['status']['phase']=='Successful', 'The AnalysisRun must be Successful'
res=run['status']['metricResults'][0]
assert res['name']=='probe-available' and res.get('successful')==1 and res['measurements'][0]['phase']=='Successful', 'The metric must have one successful measurement'
