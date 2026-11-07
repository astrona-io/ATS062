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

t=obj('analysistemplate','probe-args')
assert any(a['name']=='service' and 'value' not in a for a in t['spec'].get('args',[])), 'The template needs an argument service with no default'
m=t['spec']['metrics'][0]
assert m['name']=='probe-up' and m.get('count')==1 and 'job' in m['provider'], 'The template must define the job metric probe-up with count 1'
cmd=json.dumps(m['provider']['job']['spec'])
assert '{{ args.service }}' in cmd or '{{args.service}}' in cmd, 'The Job command must use the service argument'
assert 'probe-ready' in cmd, 'The Job command must assert that the body contains probe-ready'
run=obj('analysisrun','manual-run')
assert any(a['name']=='service' and a.get('value')=='probe' for a in run['spec'].get('args',[])), 'The run must set service to probe'
assert run['status']['phase']=='Successful', 'The AnalysisRun must be Successful'
res=run['status']['metricResults'][0]
assert res['name']=='probe-up' and res.get('successful')==1 and res['measurements'][0]['phase']=='Successful', 'The metric probe-up must have one successful measurement'
assert not items('rollouts'), 'No Rollout may exist'
