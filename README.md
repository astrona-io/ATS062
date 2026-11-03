# Argo Rollouts (ATS062)

Certified Argo Project Associate (CAPA): Argo Rollouts, worth 18% of the official curriculum. This course belongs to ATP012.

Each section has two modules. A module has a landing page, four parts, a summary, an ungraded playground and a graded lab. Each section ends with a capstone lab and a knowledge check, and a final domain quiz covers all three sections. All content is draft.

## Course Outline

| Section / module | Module | Parts |
| --- | --- | --- |
| 010 / 01 | Rollout Resource, ReplicaSets And Revisions | The Rollout Resource And Its Controller; ReplicaSets, Hashes And Revisions |
| 010 / 02 | Operating Rollouts And Migrating From A Deployment | Reading Status And Controlling A Release; Migrating A Deployment And Routing Traffic |
| 020 / 01 | Blue-Green Deployments | Active And Preview Services; Promotion, Analysis Hooks And Rollback |
| 020 / 02 | Canary Deployments | Steps, Weights And Replica Counts; Traffic Routing, Controlling A Canary And Choosing A Strategy |
| 030 / 01 | AnalysisTemplates And Metric Providers | The Template, Its Arguments And Its Metrics; Providers And Measurement Results |
| 030 / 02 | AnalysisRuns And Rollout Integration | The AnalysisRun Lifecycle And Where A Rollout Runs It; How A Result Changes The Rollout, And Experiments |

## Author Review

See [curriculum coverage](CURRICULUM.md), [primary sources](SOURCES.md), [question-bank documentation](ASSESSMENTS.md) and [contribution instructions](CONTRIBUTING.md).

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
| 030/capstone | Analysis Capstone: Block A Bad Release With Background Analysis |
