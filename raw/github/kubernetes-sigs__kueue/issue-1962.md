# Issue #1962: [metrics] Add Kueue scheduler preemption metrics

**Summary**: [metrics] Add Kueue scheduler preemption metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1962

**Last updated**: 2024-04-12T08:07:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-09T12:45:46Z
- **Updated**: 2024-04-12T08:07:16Z
- **Closed**: 2024-04-12T08:07:15Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, there are no Scheduler metrics for preemption. 

Proposed metrics:
- `PreemptedWorkloadsTotal` (counter by analogy to `AdmittedWorkloadsTotal`)
- `PreemptionAttemptsTotal`     (counter by analogy to the kube-scheduler metric  [PreemptionAttempts](https://github.com/kubernetes/kubernetes/blob/9791f0d1f39f3f1e0796add7833c1059325d5098/pkg/scheduler/metrics/metrics.go#L95-L101)

**Why is this needed**:

This is inspired by the scalability tests in https://github.com/kubernetes-sigs/kueue/issues/1912. 

We need some observability for Job-level preemptions by Kueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T12:49:18Z

/cc @alculquicondor @tenzen-y WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-09T15:17:49Z

> PreemptedWorkloadsTotal

This one is being added in #1955

> PreemptionAttemptsTotal

This could be useful to understand the performance.

> SchedulingCycleDuration

We have `admission_attempt_duration_seconds`. But we might want to add some granularity for certain steps (like preemption calculation).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-10T09:28:50Z

> > PreemptedWorkloadsTotal
> 
> This one is being added in #1955
> 
> > PreemptionAttemptsTotal
> 
> This could be useful to understand the performance.
> 
> > SchedulingCycleDuration
> 
> We have `admission_attempt_duration_seconds`. But we might want to add some granularity for certain steps (like preemption calculation).

SGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-11T19:26:08Z

> > PreemptedWorkloadsTotal
> 
> This one is being added in #1955

I see, I missed `admissionAttemptDuration` (the analog of `SchedulingCycleDuration`), this metric along with `evicted_workloads` covers already 90% of the original scope. 

> > SchedulingCycleDuration
> 
> We have `admission_attempt_duration_seconds`. But we might want to add some granularity for certain steps (like preemption calculation).

I  think that we don't need more granularity into preemption calculations at this moment.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-11T19:29:52Z

I'm hesitant regarding `PreemptionAttemptsTotal`. It will be mostly redundant to EvictedWorkloads[reason=Preempted], but maybe useful if the preemption attempts are retried continuously.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-12T08:07:11Z

/close
Let's close for now, as the original plan is mostly covered as per https://github.com/kubernetes-sigs/kueue/issues/1962#issuecomment-2050369243

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-12T08:07:16Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1962#issuecomment-2051236476):

>/close
>Let's close for now, as the original plan is mostly covered as per https://github.com/kubernetes-sigs/kueue/issues/1962#issuecomment-2050369243


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
