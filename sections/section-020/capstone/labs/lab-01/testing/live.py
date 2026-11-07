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
def env_of(rollout):
 return {e['name']:e.get('value') for e in rollout['spec']['template']['spec']['containers'][0].get('env',[])}

r=obj('rollout','scout'); st=r['status']; bg=r['spec']['strategy']['blueGreen']
assert bg.get('activeService')=='scout-active' and bg.get('previewService')=='scout-preview', 'activeService and previewService are wrong'
assert bg.get('autoPromotionEnabled') is not False, 'Automatic promotion must stay enabled'
pre=bg.get('prePromotionAnalysis',{})
assert pre.get('templates',[{}])[0].get('templateName')=='probe-gate', 'prePromotionAnalysis must use the template probe-gate'
assert env_of(r).get('REVISION')=='two', 'Revision two must be applied to scout'
assert observed(r) and st.get('phase')=='Healthy', 'scout must be Healthy after the promotion'
assert st.get('stableRS')==st.get('currentPodHash'), 'The new ReplicaSet of scout must be stable'
assert r['metadata']['annotations'].get('rollout.argoproj.io/revision')=='2', 'Revision 2 of scout must be current'
active=obj('service','scout-active')
assert active['spec']['selector'].get('rollouts-pod-template-hash')==st['currentPodHash'], 'scout-active must select the new ReplicaSet'
runs=[x for x in items('analysisruns') if owned_by(x,'Rollout','scout')]
assert runs and any(x['status'].get('phase')=='Successful' and x['status'].get('metricResults',[{}])[0].get('name')=='probe-ok' for x in runs), 'scout must own a Successful pre-promotion AnalysisRun'

m=obj('rollout','mission'); st=m['status']; c=m['spec']['strategy']['canary']
assert c.get('stableService')=='mission-stable' and c.get('canaryService')=='mission-canary', 'stableService and canaryService are required'
assert c.get('trafficRouting',{}).get('nginx',{}).get('stableIngress')=='mission-ingress', 'trafficRouting.nginx.stableIngress must be mission-ingress'
assert c.get('dynamicStableScale') is True, 'dynamicStableScale must be true'
steps=c.get('steps',[])
assert steps and steps[0].get('setCanaryScale',{}).get('replicas')==1, 'The first step must be setCanaryScale with replicas 1'
assert any(s.get('setWeight')==50 for s in steps) and steps[-1].get('setWeight')==100, 'The steps must set weight 50 and end with setWeight 100'
assert env_of(m).get('REVISION')=='two', 'Revision two must be applied to mission'
assert observed(m) and st.get('phase')=='Healthy' and st.get('readyReplicas')==2, 'mission must be Healthy with 2 ready replicas'
assert st['currentPodHash']!=obj('configmap','initial-mission')['data']['hash'], 'The initial revision of mission was never replaced'
assert st.get('stableRS')==st['currentPodHash'], 'The new ReplicaSet of mission must be stable'
assert m['metadata']['annotations'].get('rollout.argoproj.io/revision')=='2', 'Revision 2 of mission must be current'
i=obj('ingress','mission-mission-ingress-canary')
assert owned_by(i,'Rollout','mission'), 'The canary Ingress must be owned by the Rollout'
assert i['metadata'].get('annotations',{}).get('nginx.ingress.kubernetes.io/canary')=='true', 'The canary Ingress must carry the canary annotation'
