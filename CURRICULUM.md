# Curriculum Coverage

Exam: Certified Argo Project Associate (CAPA). Domain: Argo Rollouts (18%).

The [official objectives](https://training.linuxfoundation.org/certification/certified-argo-project-associate-capa/) were checked on 2026-10-11. Teaching structure is independently authored and does not add official requirements.

| Section | Official objective | Modules | Capstone | Quiz |
| --- | --- | --- | --- | --- |
| 010 | Understand Argo Rollouts Fundamentals | 2 | yes | sections/section-010/quiz.yaml |
| 020 | Use Common Progressive Rollout Strategies | 2 | yes | sections/section-020/quiz.yaml |
| 030 | Describe Analysis Template and AnalysisRun | 2 | yes | sections/section-030/quiz.yaml |

The final domain quiz is sections/final-domain-quiz.yaml.

| Section / module | Module | Parts |
| --- | --- | --- |
| 010 / 01 | Rollout Resource, ReplicaSets And Revisions | The Rollout Resource And Its Controller; ReplicaSets, Hashes And Revisions; Timing, Capacity And History Fields; Template Changes, Metadata And Placement |
| 010 / 02 | Operating Rollouts And Migrating From A Deployment | Reading Status And Controlling A Release; Migrating A Deployment And Routing Traffic; Observing A Release: Events, Logs And Metrics; Failed Releases And Recovery |
| 020 / 01 | Blue-Green Deployments | Active And Preview Services; Promotion, Analysis Hooks And Rollback; Scale-Down And Preview Behaviour; Operating A Blue-Green Rollout |
| 020 / 02 | Canary Deployments | Steps, Weights And Replica Counts; Traffic Routing, Controlling A Canary And Choosing A Strategy; Canary Scale Control; Header Routing And Mirroring |
| 030 / 01 | AnalysisTemplates And Metric Providers | The Template, Its Arguments And Its Metrics; Providers And Measurement Results; Cluster Templates And Argument Sources; Dry Run, Retention And Error Handling |
| 030 / 02 | AnalysisRuns And Rollout Integration | The AnalysisRun Lifecycle And Where A Rollout Runs It; How A Result Changes The Rollout, And Experiments; Passing Rollout Data Into An Analysis; Reading And Debugging An AnalysisRun |

AUTHORING.yaml records the objectives and the labs per module. All technical readings remain draft. Live verification is recorded separately and is pending.

## Hands-On Coverage

This course has 6 ungraded playgrounds, 12 module labs (two for each module) and 3 capstone labs. Each lab task follows the parts it practises, and the solution is not listed as a reading. Static checks (`astrona validate`, `bash -n`, YAML and JSON parsing) are done. No lab or playground has been run on a cluster, so all are untested.

| Section / module | Graded lab |
| --- | --- |
| 010/01 | Reconcile A Rollout And Its ReplicaSet |
| 010/02 | Migrate A Deployment To A Rollout With workloadRef |
| 010/capstone | Fundamentals Capstone: Run And Update A Rollout Behind A Service |
| 020/01 | Hold A Blue-Green Revision In Preview |
| 020/02 | Complete A Canary Revision With Weight And Pause Steps |
| 020/capstone | Strategies Capstone: Preview A Blue-Green Release And Complete A Canary |
| 030/01 | Execute A Job-Based Analysis |
| 030/02 | Gate A Canary Step With An AnalysisRun |
| 010/01 (lab 2) | Set Timing Fields And Stable Metadata On A Rollout |
| 010/02 (lab 2) | Set A Progress Deadline With Automatic Abort |
| 020/01 (lab 2) | Run A Blue-Green Rollout With A Small Preview |
| 020/02 (lab 2) | Limit Surge And Unavailability In A Canary |
| 030/01 (lab 2) | Try A Metric In Dry Run |
| 030/02 (lab 2) | Run An AnalysisRun With An Argument |
| 030/capstone | Analysis Capstone: Block A Bad Release With Background Analysis |
