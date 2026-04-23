# Issue #9223: Set thresholds for TAS performance test

**Summary**: Set thresholds for TAS performance test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9223

**Last updated**: 2026-02-27T16:45:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ASverdlov](https://github.com/ASverdlov)
- **Created**: 2026-02-13T14:57:57Z
- **Updated**: 2026-02-27T16:45:42Z
- **Closed**: 2026-02-27T16:45:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ASverdlov](https://github.com/ASverdlov)
- **Comments**: 6

## Description

**What would you like to be cleaned**:
Calibrate the TAS performance test thresholds (`rangespec.yaml`) based on actual CI execution history. The current thresholds are placeholder values (`10_000_000` ms) that effectively disable regression detection.

**Why is this needed**:
PR #8917 added a TAS performance test with provisional thresholds. The corresponding CI job was added in
https://github.com/kubernetes/test-infra/pull/36375. The plan was to let the test run in CI for some time, collect timing data, and then set meaningful thresholds — similarly to how the baseline test thresholds were calibrated from 5 trial runs (see `configs/baseline/rangespec.yaml`).

**Proposed plan**
1. Collect data from ~10+ CI runs of the TAS performance test
2. Compute average and variance for each metric (wall time, queue usage, per-class admission time)
3. Set thresholds with appropriate margins (following the baseline pattern: avg + 20-35% for time, avg - 5-7% for usage)
4. Update `test/performance/scheduler/configs/tas/rangespec.yaml` with the calibrated values

/kind cleanup
/area testing

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-13T14:58:01Z

@ASverdlov: The label(s) `area/testing` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9223):

>**What would you like to be cleaned**:
>Calibrate the TAS performance test thresholds (`rangespec.yaml`) based on actual CI execution history. The current thresholds are placeholder values (`10_000_000` ms) that effectively disable regression detection.
>
>**Why is this needed**:
>PR #8917 added a TAS performance test with provisional thresholds. The corresponding CI job was added in
>https://github.com/kubernetes/test-infra/pull/36375. The plan was to let the test run in CI for some time, collect timing data, and then set meaningful thresholds — similarly to how the baseline test thresholds were calibrated from 5 trial runs (see `configs/baseline/rangespec.yaml`).
>
>**Proposed plan**
>1. Collect data from ~10+ CI runs of the TAS performance test
>2. Compute average and variance for each metric (wall time, queue usage, per-class admission time)
>3. Set thresholds with appropriate margins (following the baseline pattern: avg + 20-35% for time, avg - 5-7% for usage)
>4. Update `test/performance/scheduler/configs/tas/rangespec.yaml` with the calibrated values
>
>/kind cleanup
>/area testing


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-13T16:25:53Z

It's difficult to come up with non-flaky thresholds right now as TAS performance test stats show a very high variance compared to average ([CV](https://en.wikipedia.org/wiki/Coefficient_of_variation)) for admission times across test runs (up to 30%). It looks like we don't have enough workloads in the generator configuration for some workload patterns to reduce that variance.

Checkout the numbers for both TAS and baseline perf tests I calculated with a script that fetches `summary.yaml` files for the last ~20 test runs from Prow and calculates the metrics in the [the gist](https://gist.github.com/ASverdlov/45d12b2c689106789ed78f156f586e2a).

Notice:
TAS - lower workload counts correlate with higher CV%:
  - 60 workloads (large-balanced-rack) → 37.1% CV
  - 90 workloads (medium-balanced-rack) → 34.7% CV
  - 120 workloads (medium-preferred-block) → 32.3% CV
  - 180 workloads (medium/small-required/preferred-rack) → ~9% CV
  - 300 workloads (small-required-rack) → 5.3% CV

Baseline - much higher counts, much lower CV%:
  - 1,500 / 3,000 / 10,500 workloads → 1.9–14.1% CV

I propose to increase the workload counts for the TAS config (`test/performance/scheduler/configs/tas/generator.yaml`) to try to reduce CV% first. Then wait another week and introduce thresholds if CV% are <= 10%.
We might also need to increase the timeout for the test from 10 minutes to e.g. 20 minutes to allow for more workloads to be processed.

cc @mimowo

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-13T21:18:01Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T16:09:26Z

@ASverdlov any update here? I believe we should already have enough data

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-25T16:12:17Z

Hey @mimowo 
I'll take a look today!

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-25T23:55:03Z

The admission time volatility is much better now (CV% < 5)! Created a PR with setting the thresholds ^
