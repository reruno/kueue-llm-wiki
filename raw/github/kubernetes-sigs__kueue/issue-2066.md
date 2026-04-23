# Issue #2066: Scalability test is flaky

**Summary**: Scalability test is flaky

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2066

**Last updated**: 2024-04-26T15:03:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-25T14:58:01Z
- **Updated**: 2024-04-26T15:03:39Z
- **Closed**: 2024-04-26T15:03:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

**What happened**:

It flaked on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2047/pull-kueue-test-scheduling-perf-main/1783505231846313984

**What you expected to happen**:

Not flake

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build on CI

**Anything else we need to know?**:

The asserts were only recently added so they may need tuning: https://github.com/kubernetes-sigs/kueue/pull/2043

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-25T14:58:08Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-04-25T15:07:55Z

I'll relax the asserts tomorrow.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-25T15:35:44Z

I'm wondering on the methodology though. I think if we have a dozen of runs we could fit the normal distribution per stat and set the threshold to the tail of the distribution where the expected ratio of failures is below 1/1000.

EDIT: or another constant ratio, but 1/100 seems too common.

### Comment by [@trasc](https://github.com/trasc) — 2024-04-25T16:07:04Z

let's try $2067

> I'm wondering on the methodology though. I think if we have a dozen of runs we could fit the normal distribution per stat and set the threshold to the tail of the distribution where the expected ratio of failures is below 1/1000.

There ware used 5 test runs to to propose the values and additional runs ware done (very likely close to 12, at different times of day) .

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T10:01:45Z

Based  on the flake I tried manually the approach for determining the threshold as 99.999 percentile of a fit normal distribution, based on 10 last successful builds from https://prow.k8s.io/job-history/gs/kubernetes-jenkins/pr-logs/directory/pull-kueue-test-scheduling-perf-main. For fitting the distribution I used manually https://agrimetsoft.com/distributions-calculator/normal-distribution-fitting, and for percentile: https://www.wolframalpha.com/widgets/gallery/view.jsp?id=67817f2e01eecd366e6d73ac7a71bcd1.

This yields the following results below. It is encouraging approach seems it discovered the metrics for large workloads and sys time which were flaking.

SysTime:
29293
29628
25351
24844
29621
25119
24230
28569
21400
26554

Mean = μ: 26460.9
Standard Deviation = σ: 2763.389
**99.999-percentile: 38200, current value: 34_000 <-- I saw flakes here**

WallTime:
345999
350241
356798
355190
356002
355711
353628
355810
351334
348201
Mean = μ: 352891.4
Standard Deviation = σ: 3744.433
99.999-percentile: 369000, current value: 368000

MaxRss
444208
435012
448216
443800
447752
448876
445904
442616
441776
443900
Mean = μ: 444206
Standard Deviation = σ: 4035.501
99.999-percentile: 461000, current value: 468000

large
5929
7154
7512
6705
7628
5124
5978
7116
7800
6817
Mean = μ: 6776.3
Standard Deviation = σ: 860.536
**99.999-percentile: 10400, current value: 8000 <-- I saw flakes here**

medium:
74954
78645
77566
79381
79224
74602
76650
78053
79483
76227
Mean = μ: 77478.5
Standard Deviation = σ: 1803.784
99.999-percentile: 85200, current value: 81000

small
212656
216857
216310
220536
217552
215133
217250
217293
217459
213282
Mean = μ: 216432.8
Standard Deviation = σ: 2276.107
99.999-percentile: 226000, current value: 227000

Note that, the sample size was small, because it was done manually, but it already proved useful to surface thresholds which are too low. If we automate it we can use all available successful main builds.
