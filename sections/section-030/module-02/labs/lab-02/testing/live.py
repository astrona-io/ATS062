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
cmd=json.dumps(t['spec']['metrics'][0]['provider']['job']['spec'])
assert '{{ args.service }}' in cmd or '{{args.service}}' in cmd, 'The Job command must use the service argument'
run=obj('analysisrun','manual-run')
assert any(a['name']=='service' and a.get('value')=='probe' for a in run['spec'].get('args',[])), 'The run must set service to probe'
assert run['status']['phase']=='Successful', 'The AnalysisRun must be Successful'
assert run['status']['metricResults'][0]['name']=='probe-up', 'The metric result for probe-up is missing'
