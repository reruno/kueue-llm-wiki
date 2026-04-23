# Issue #1737: Optimize integration test suite

**Summary**: Optimize integration test suite

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1737

**Last updated**: 2024-03-05T13:24:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-14T17:28:36Z
- **Updated**: 2024-03-05T13:24:45Z
- **Closed**: 2024-03-05T13:24:43Z
- **Labels**: `kind/feature`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We need to run the entire suite, find the longer running jobs and check for opportunities for optimization.
We can also look into running some tests in parallel, although that might not be possible in most scenarios, as CQs are non-namespaced. Unless we use different cohorts?

Removing some tests in favor of unit cases is also an option, when there is no additional benefit from the test.

**Why is this needed**:

The suite is starting to take too long.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-16T12:37:31Z

Maybe we could start by optimizing the longest suites
```
> grep -e "Specs in" -e "Running Suite"  < build-log.txt
Running Suite: Provisioning admission check suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning
Ran 8 of 8 Specs in 73.603 seconds
Running Suite: Core Controllers Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/core
Ran 22 of 22 Specs in 93.300 seconds
Running Suite: Job Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/job
Ran 39 of 40 Specs in 104.881 seconds
Running Suite: JobSet Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/jobset
Ran 10 of 10 Specs in 47.849 seconds
Running Suite: MPIJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/mpijob
Ran 12 of 12 Specs in 47.200 seconds
Running Suite: MXJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/mxjob
Ran 6 of 6 Specs in 31.343 seconds
Running Suite: PaddleJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/paddlejob
Ran 6 of 6 Specs in 32.231 seconds
Running Suite: Pod Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/pod
Ran 19 of 19 Specs in 49.266 seconds
Running Suite: PyTorchJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/pytorchjob
Ran 9 of 9 Specs in 44.959 seconds
Running Suite: RayCluster Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/raycluster
Ran 9 of 9 Specs in 66.868 seconds
Running Suite: RayJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/rayjob
Ran 10 of 10 Specs in 67.749 seconds
Running Suite: TFJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/tfjob
Ran 6 of 6 Specs in 32.547 seconds
Running Suite: XGBoostJob Controller Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/xgboostjob
Ran 6 of 6 Specs in 32.331 seconds
Running Suite: Multikueue Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue
Ran 4 of 4 Specs in 29.872 seconds
Running Suite: Scheduler Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler
Ran 53 of 53 Specs in 106.653 seconds
Running Suite: Scheduler with WaitForPodsReady Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready
Ran 11 of 11 Specs in 147.965 seconds
Running Suite: Webhook Suite - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/webhook
Ran 40 of 40 Specs in 13.822 seconds
```
This is 17min total currently.

The winner is `Scheduler with WaitForPodsReady Suite`. Probably due to the use of sleeps to exceed the timeouts. Maybe the sleep time can be optimized, or we can move some of the scenarios to unit tests as suggested, maybe both strategies.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-16T14:31:45Z

/assign @mimowo

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-02-20T09:55:51Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-02-21T12:07:03Z

I tested running specs within suites in parallel by adding the flag [-procs=N](https://onsi.github.io/ginkgo/#spec-parallelization) at commit fa96518c293473480b0d1f45f642af23e433302e, running on a n2d-standard-48. Times below are in seconds.
Suite / Parallelism | N=1 | N=2 | N=4 | N=8 | N=16
-- | -- | -- | -- | -- | --
Provisioning admission check suite | 15.6 | 15.1 | 17.7 | 15.3 | 15.8
Core Controllers Suite | 85.5 | 48.4 | 28.7 | 28.2 | 30.1
Job Controller Suite | 94.1 | 57.7 | 44.6 | 44.0 | 45.3
JobSet Controller Suite | 40.6 | 22.7 | 15.8 | 10.2 | 10.1
MPIJob Controller Suite | 42.0 | 22.3 | 14.7 | 9.3 | 9.5
MXJob Controller Suite | 26.8 | 15.6 | 10.3 | 9.5 | 9.2
PaddleJob Controller Suite | 25.0 | 16.7 | 9.1 | 9.3 | 9.5
Pod Controller Suite | 43.9 | 32.1 | 27.6 | 27.2 | 27.9
PyTorchJob Controller Suite | 35.6 | 18.1 | 10.1 | 9.7 | 9.4
RayCluster Controller Suite | 53.3 | 26.5 | 18.8 | 10.5 | 10.5
RayJob Controller Suite | 51.9 | 26.7 | 19.6 | 10.1 | 10.8
TFJob Controller Suite | 26.6 | 16.1 | 9.5 | 10.5 | 9.8
XGBoostJob Controller Suite | 25.4 | 16.2 | 10.0 | 8.7 | 9.2
Multikueue Suite | 25.5 | 22.0 | 20.3 | 19.9 | 18.6
Scheduler Suite | 102.7 | 54.9 | 32.6 | 19.9 | 15.4
Scheduler with WaitForPodsReady Suite | 132.9 | 65.7 | 40.8 | 28.8 | 22.2
Webhook Suite | 11.6 | 8.4 | 7.8 | 7.7 | 7.4
-- | -- | -- | -- | -- | --
Total Time | 839.2 | 485.5 | 337.9 | 278.6 | 270.7
Time as fraction of baseline | 1.00 | 0.58 | 0.40 | 0.33 | 0.32
Time as fraction of previous |   | 0.58 | 0.70 | 0.82 | 0.97

Given that the the speedup with more parallelism is marginal, and that the [test environment requests 4 cpus](https://github.com/kubernetes/test-infra/blob/21cac776063ef0a3ca42476059b2206895409075/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L55-L60), I recommend the option N=4.

At higher parallelism (N=32), I encountered the suite failing due to file descriptors being exhausted while running the Multikueue Suite; there is the risk that this will be an issue at lower parallelism in the integration test environment.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-21T12:45:38Z

Nice results! I'm yet wondering if we are safe to run them in parallel, because some resources like CQ are global. I suppose in that case we are running multiple API servers, and etcds at different ports, can you confirm? Running multiple api servers and etcds could probably explain why we run out of file descriptors at high N. If we are safe, and the environments are disjoint, then N=4 sounds as a reasonable choice.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-02-21T15:19:16Z

I confirmed: we are running multiple API servers and etcds on different ports.

Regarding the fds running out, I looked deeper and found that Ginkgo will run BeforeSuite for each process, even if there are more processes than specs. In the [Multikueue suite's BeforeSuite](https://github.com/kubernetes-sigs/kueue/blob/fa96518c293473480b0d1f45f642af23e433302e/test/integration/multikueue/suite_test.go#L110-L114), we create 3 api servers/etcds for each process, so it's easy to imagine how we ran out of fds when N=32.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-21T15:53:01Z

Can you upload a PR to see how it behaves in the bot?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-21T15:53:15Z

Right, in that case making the suites run in parallel is no-brainer :) Getting down to 6min will be a win. I would just suggest to make it parameterized and feel free to submit a PR. Also, we may check if it is possible to have a separate log artifact per suite / or process.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-03-05T08:57:38Z

Looked at recent successful runs. Down from 10m11s (n=13) to 8m51s (n=12) after increasing requests/limits in https://github.com/kubernetes/test-infra/pull/32150

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-05T13:24:39Z

It sounds like that's as far as we'll get with increased limits.

Let's leave this here. Thanks!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-05T13:24:44Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1737#issuecomment-1978771704):

>It sounds like that's as far as we'll get with increased limits.
>
>Let's leave this here. Thanks!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
