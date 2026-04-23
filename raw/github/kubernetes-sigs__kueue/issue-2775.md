# Issue #2775: Making perftest threshhold to be more plausible

**Summary**: Making perftest threshhold to be more plausible

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2775

**Last updated**: 2024-10-08T06:36:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-08-05T16:58:03Z
- **Updated**: 2024-10-08T06:36:03Z
- **Closed**: 2024-10-08T06:36:02Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to improve the perftest threshold to be more plausible.

We can consider updating the https://github.com/kubernetes-sigs/kueue/blob/f05e359497d30a0f90e98da0bad9e99bf38fe919/test/performance/scheduler/default_rangespec.yaml in the following 3 options:

1. Automatically update the threshold by sampling the mid/average values against every PR proposed in https://github.com/kubernetes-sigs/kueue/issues/2077.
2. Manually update the threshold periodically, like once a month.
3. Keep relaxing the threshold based on the flaky test alert.

xref: https://github.com/kubernetes-sigs/kueue/pull/2758#issuecomment-2264755030

**Why is this needed**:
The current perftest is slightly unstable, and we often relax the threshold for the perftest. 
But, we may miss the regressions by repeatedly relaxing the threshold.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-05T16:59:07Z

cc: @mimowo @trasc @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-05T17:34:26Z

> Automatically update the threshold by sampling the mid/average values against every PR proposed in https://github.com/kubernetes-sigs/kueue/issues/2077.

The script is just to collect the data quickly (now collected manually). It is another decision how we use the data.
I think it could be helpful to:
1. set up the initial threshold as the 99.999 percentile, so a build failure is expected 1/10000
2. see if this is false positive or true positive (regression), by drawing the trends of build time on the x-axis and measured value on the y-axis

For (2.) the idea is that after a couple of days since the first failure we would see if the graph returned to the historical data, or if there is some systematic increase.

This strategy could be combined with "Keep relaxing the threshold based on the flaky test alert.".

### Comment by [@trasc](https://github.com/trasc) — 2024-08-06T15:16:13Z

In my o pinion the biggest issue for us in that the test-infra is not very consistent, one approach we can experiment with can be to run our scenario multiple times and do some kind of aggregated check (verify the average values, have at least n runs pass or something similar). 

Other things that we should take into account:
- a pure statistical model may not be that relevant if the input data is coming from running different code
- a "real" (that is not based on interpolation) P99.999 can be computed only if we have more then 100000 items in the dataset
- if we continue to just increase the thresholds without identifying a reason for the regression it's not an indication that a regression did not happen.

### Comment by [@trasc](https://github.com/trasc) — 2024-08-09T11:40:25Z

#2810 Adds a script that can be used to run ' run-performance-scheduler' multiple times on two distinct git revisions in a environment more stable then CI infra (maybe local PC) to check if a regression on CI is related to the code or to the the CI infra.

### Comment by [@trasc](https://github.com/trasc) — 2024-08-12T08:46:59Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-scheduling-perf-main/1822456340883181568 failed over thw weekend, but is the 1 in 5 runs using the same code, the major difference is that in that casa the we see some evictions taking place (30 for medium and 87 for small).

We can think of changing the generation setup either: 
1. Avoid evictions 
2. Always have evictions

In my opinion 2 is better since eviction is a normal behavior for kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-08T06:35:58Z

I believe we can close it for now as:
1. we have the retry mechanism: https://github.com/kubernetes-sigs/kueue/pull/3020
2. the board is clean for 2 weeks: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-scheduling-perf-main, but there hasn't been a failure since the retry probably

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-08T06:36:02Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2775#issuecomment-2398970000):

>I believe we can close it for now as:
>1. we have the retry mechanism: https://github.com/kubernetes-sigs/kueue/pull/3020
>2. the board is clean for 2 weeks: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-scheduling-perf-main, but there hasn't been a failure since the retry probably
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
