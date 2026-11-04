---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Describe Analysis Template and AnalysisRun

This section covers automated release decisions. An AnalysisTemplate defines metrics and providers, and an AnalysisRun measures them. A Rollout runs analysis in a canary step, in the background and around blue-green promotion, and the result continues, pauses or aborts the release.

## Modules

1. AnalysisTemplates And Metric Providers
2. AnalysisRuns And Rollout Integration
3. Experiments
4. Analysis Providers In Depth

Each module has a short landing page, up to four parts and a summary. A playground and a graded lab follow the parts. The section ends with a capstone lab and a knowledge check.

## Learning Outcomes

- Write a template with arguments, metrics, conditions and limits.
- Choose the job, web or prometheus provider.
- Describe the AnalysisRun lifecycle and the effect of each phase on a Rollout.
- Describe what an Experiment adds.
- Run an Experiment on its own and inside a canary step, and read its status.
- Configure the web, Prometheus and vendor providers, and write success, failure and inconclusive conditions.
