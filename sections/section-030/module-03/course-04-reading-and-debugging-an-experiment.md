---
draft: true
exam_objectives:
- Describe Analysis Template and AnalysisRun
---
# Reading And Debugging An Experiment

An experiment is short and its pods disappear, so the evidence is easy to lose. This part shows the fields to read while the experiment runs and after it ends, and the usual reasons for a failure.

## The status of an experiment

The status of an experiment has three useful groups of fields. The `phase` and `message` give the overall result. The list `templateStatuses` has one entry for each template, with its `name`, `replicas`, `readyReplicas` and a `status` such as `Running` or `Successful`. The list `analysisRuns` has one entry for each analysis, with its `name`, the name of the run and its `phase`.

<!-- astrona:playground:renew -->

Read them with `kubectl`:

```sh
kubectl -n starfleet get experiment compare -o jsonpath='{.status.phase} {.status.message}{"\n"}'
kubectl -n starfleet get experiment compare -o jsonpath='{range .status.templateStatuses[*]}{.name} {.status}{"\n"}{end}'
kubectl -n starfleet get experiment compare -o jsonpath='{range .status.analysisRuns[*]}{.name} {.phase}{"\n"}{end}'
```

The first command prints the result. The second prints one line for each template, and the third prints one line for each analysis. If the experiment named `compare` does not exist in your playground, use the name of the experiment you created.

## Events and conditions

`kubectl describe experiment compare` prints the conditions and the events at the end. The events record when the ReplicaSets were created and scaled, and when the analyses started. Read them in order, because the first error is usually the cause.

## Common reasons for a failure

The reasons fall into a few groups.

- **A template never became available.** The image could not be pulled, or a pod stayed `Pending`. The experiment fails after `progressDeadlineSeconds`. Read the pods and their events.
- **An analysis failed.** Read the `AnalysisRun` named in the status, as described for any run: the phase of each metric and the measurements.
- **The spec is invalid.** The selector does not match the template labels, or two templates have the same name. The phase is `Error` and the message names the problem.
- **The analysis template is missing.** The analysis entry names a template that does not exist in the namespace. The run cannot be created.

## After the experiment

The experiment object stays after it ends, with its status. The `AnalysisRun` objects stay too, because the experiment owns them. Deleting the experiment deletes both. A canary experiment is owned by the Rollout, and the history limits of the Rollout remove old ones.

## What you know now

The status of an experiment holds the phase, the template statuses and the analysis runs. Events and the owned runs give the details of a failure. The module closes with the main points.

## Common pitfalls

> [!WARNING]
> The pods of an experiment are scaled down at the end, so a log request after the end returns nothing. Read the logs while it runs, or use an analysis that stores its result in the measurements.
