# Issue #2993: Revisit optimizing the integration test runtime

**Summary**: Revisit optimizing the integration test runtime

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2993

**Last updated**: 2024-10-03T05:56:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-05T12:53:38Z
- **Updated**: 2024-10-03T05:56:50Z
- **Closed**: 2024-10-03T05:56:48Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 35

## Description

We have had an effort to improve the integration test performance in the past, and we've taken down the time below 10min.

However, recently the integration tests suite takes over 16min based on https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main. Specific example: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1831572082656284672

Part of the effort would be to figure out if the slow down can be attributed to more tests, or there is another reason.

The build time is important particularly during release process which takes a couple of builds.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T12:53:51Z

/cc @tenzen-y @alculquicondor @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T07:13:52Z

FYI the previous effort (for x-ref): https://github.com/kubernetes-sigs/kueue/issues/1737

### Comment by [@trasc](https://github.com/trasc) — 2024-09-10T07:41:38Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T15:57:09Z

Actually, I proposed refactoring the MultiKueue Kubeflow E2E and integration testing.
@mszadkow How about progressing?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T16:25:46Z

@tenzen-y what is the aim of the refactoring, can you point to the discussion? How will this impact the integration test performance?

Also, before we start optimizing the status quo, I would really appreciate investigation why the time increased from 9min to 16min since https://github.com/kubernetes-sigs/kueue/issues/1737#issuecomment-1978255495, which was just 6 months ago. It could be just due to new tests, but maybe there is something else responsible (like slower machines or performance regression).

EDIT: what I mean by that is we can check first what the new integration tests added since then, and if they can really account for the additional 7min - I'm surprised by the increase just within 6 months. Maybe some of the new tests are not optimized.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-13T06:59:15Z

For starters I propose #3035 which adds a way to report the time taken by individual tests.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-13T07:24:15Z

When it comes to overall time consumption the trend was fairly study, the biggest bump (of around 2min) I see is around [05 Jul](https://prow.k8s.io/job-history/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main?buildId=1809099295970824192) when race detection was added.

```bash
$ git log 35586d7539bff45e071d39f7e85ebc87e4245c97..cd89852f2c4d921e2ec51917152f8fdea80eb87d
commit cd89852f2c4d921e2ec51917152f8fdea80eb87d
Author: Irving Mondragón <IrvingMg@users.noreply.github.com>
Date:   Thu Jul 4 22:51:06 2024 +0200

    Remove deprecated Hugo template (#2506)

commit 6c619c6becea43415bb189067c5e94e8dcda355f
Author: Mykhailo Bobrovskyi <mikhail.bobrovsky@gmail.com>
Date:   Thu Jul 4 20:48:06 2024 +0300

    Runs the race detector on integration tests. (#2468)

```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-13T10:29:52Z

I think the race detection proved to be useful already, so the trade off is not clear to me. I would keep it for now, but just keep in mind that we could gain 2min on changing it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T11:01:27Z

> @tenzen-y what is the aim of the refactoring, can you point to the discussion? How will this impact the integration test performance?
> 
> Also, before we start optimizing the status quo, I would really appreciate investigation why the time increased from 9min to 16min since https://github.com/kubernetes-sigs/kueue/issues/1737#issuecomment-1978255495, which was just 6 months ago. It could be just due to new tests, but maybe there is something else responsible (like slower machines or performance regression).
> 
> EDIT: what I mean by that is we can check first what the new integration tests added since then, and if they can really account for the additional 7min - I'm surprised by the increase just within 6 months. Maybe some of the new tests are not optimized.

@mimowo Actually, I meant the following discussion:
https://github.com/kubernetes-sigs/kueue/pull/2869#discussion_r1727318416

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-13T11:10:02Z

> @mimowo Actually, I meant the following discussion:
> [#2869 (comment)](https://github.com/kubernetes-sigs/kueue/pull/2869#discussion_r1727318416)

The decision taken in this discussion sgtm, but I'm not seeing how it is related to this issue, which is focused on integration tests rather than e2e.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T11:17:46Z

> > @mimowo Actually, I meant the following discussion:
> > [#2869 (comment)](https://github.com/kubernetes-sigs/kueue/pull/2869#discussion_r1727318416)
> 
> The decision taken in this discussion sgtm, but I'm not seeing how it is related to this issue, which is focused on integration tests rather than e2e.

Oh, I was supposed to mention integration testing as well.
Because we have duplicated Kubeflow MultiKueue integration testing even though the core Kubeflow MultiKueue reconcilers are commonized and the same.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-13T11:31:52Z

I see, so your suggestion is to only keep integration tests for `PyTorchJob`, and drop for other kubeflow Jobs? I'm open to this possibility but would expect some review of the time impact, and review of the test coverage provided by unit tests for the integrations.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-13T14:49:47Z

> I see, so your suggestion is to only keep integration tests for `PyTorchJob`, and drop for other kubeflow Jobs? I'm open to this possibility but would expect some review of the time impact, and review of the test coverage provided by unit tests for the integrations.

That can be easily done but I don't expect a huge gain out of that , each of the tests are taking under 3 sec to execute.

With #3039 I tried to parallelize the cluster creation for multikueue in theory that can reduce the tome with around 40s, but making the setup thread safe is more challenging then expected.  

Another thing we can try is to reuse the envtest clusters and setup-manager / stop-manager operations, but this may not make too much difference with parallel running and surface new issues due to incomplete cleanups.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-18T05:37:01Z

- #3054

Adds the ability to reuse the envtest instance, and replace the manager.

One followup for this can be lazy star the envtest instances, this will probably have a bigger code impact and it's benefits will be visible only in suites that have a lower number of top level specs then the parallelism.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T15:41:24Z

> I see, so your suggestion is to only keep integration tests for `PyTorchJob`, and drop for other kubeflow Jobs? I'm open to this possibility but would expect some review of the time impact, and review of the test coverage provided by unit tests for the integrations.

That may be a little bit different. I'm wondering if we can add all Kubeflow MultiKueue cases only in PyTorchJob and add only basic creation cases in all other Kubeflow Jobs. That is similar to Kubeflow Jobs integration testings (not MultiKueu).

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T05:46:22Z

> That may be a little bit different. I'm wondering if we can add all Kubeflow MultiKueue cases only in PyTorchJob and add only basic creation cases in all other Kubeflow Jobs. That is similar to Kubeflow Jobs integration testings (not MultiKueu).

It is done in #3085

### Comment by [@trasc](https://github.com/trasc) — 2024-10-01T12:55:48Z

With #3085 merged
- https://github.com/kubernetes/test-infra/pull/33568
will skip the slow and redundant test in pr builds. 

With this the testing time will get from 18min to around 12min for PRs, and around 14-45min for periodic builds.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-01T16:37:50Z

Wonderful, thank you!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T16:42:39Z

> With #3085 merged
> 
> - https://github.com/kubernetes/test-infra/pull/33568
> 
> will skip the slow and redundant test in pr builds. 
> 
> 
> 
> With this the testing time will get from 18min to around 12min for PRs, and around 14-45min for periodic builds.

Great to see! Thanks! 
Will you plan to do any performance improving, or not?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-01T16:45:35Z

Ideally it would be nice to be around 10min, but maybe keeping the goal is not feasible as the project grows, so I think we can close. 

Unless @trasc you have some more ideas you want to follow up with?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T08:47:50Z

The recent https://github.com/kubernetes-sigs/kueue/pull/3176 inspires me to ask if we could re-visit reducing the podsReadyTimeout used in a couple of tests, like [here](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/podsready/scheduler_test.go#L207), or [here](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/podsready/scheduler_test.go#L694) to use the TinyTimeout rather than ShortTimeout, can you check that yet @mbobrovskyi or @trasc ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T08:53:36Z

@trasc in https://github.com/kubernetes-sigs/kueue/pull/3054 I see you introduced StartManager and used in many tests suites to optimize performance, but I see some suites still use RunManager, [example](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/fairsharing/suite_test.go#L63) from [search](https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20RunManager&type=code). Is it an omission and we should follow up, or is there a reason to keep it that way?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-02T08:58:44Z

> The recent #3176 inspires me to ask if we could re-visit reducing the podsReadyTimeout used in a couple of tests, like [here](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/podsready/scheduler_test.go#L207), or [here](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/podsready/scheduler_test.go#L694) to use the TinyTimeout rather than ShortTimeout, can you check that yet @mbobrovskyi or @trasc ?

Unfortunately, no. I already optimized this in [#2329](https://github.com/kubernetes-sigs/kueue/pull/2329), and this is the minimum we can set.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T09:00:34Z

Ack

### Comment by [@trasc](https://github.com/trasc) — 2024-10-02T09:01:32Z

> @trasc in #3054 I see you introduced StartManager and used in many tests suites to optimize performance, but I see some suites still use RunManager, [example](https://github.com/kubernetes-sigs/kueue/blob/c502e763c09601d3ffcbee6e3f82bbeb7b1cbecf/test/integration/scheduler/fairsharing/suite_test.go#L63) from [search](https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20RunManager&type=code). Is it an omission and we should follow up, or is there a reason to keep it that way?

In some suites we don't need to restart the manager with a different configuration.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T09:14:36Z

So, IIUC for these suites does not matter from performance PoV, because the manager is started only once anyway. Still, it might be worth following up to make it consistent, as people would often copy-paste the existing tests, and if they copy the ones using RunManager we may not have optimal performance in the future.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-02T11:04:18Z

> So, IIUC for these suites does not matter from performance PoV, because the manager is started only once anyway. Still, it might be worth following up to make it consistent, as people would often copy-paste the existing tests, and if they copy the ones using RunManager we may not have optimal performance in the future.

- #3179

### Comment by [@trasc](https://github.com/trasc) — 2024-10-02T11:38:55Z

One thing I wanted to check was the impact of parallelism and `--race` usage for which I did a couple of runs in #3142 and in short we have 

|                | NProcs = 4  | NProcs = 2 | NProcs = 1  | 
|----------------|-------------|------------|-------------|
| **With** `--race`    |13m24s [1841394016327831552](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841394016327831552)|12m38s [1841397714319839232](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841397714319839232)|14m59s [1841401466707775488](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841401466707775488)| 
| **Without** `--race` |10m17s [1841432977301573632](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841432977301573632)|10m40s [1841429657497374720](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841429657497374720)|12m43s [1841424736974802944](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3142/pull-kueue-test-integration-main/1841424736974802944)| 

- The overhead of `--race` is around 2min.
- The benefit of using a parallelism > 2 is limited

So besides maybe dropping the `--race` in PR builds, which may not be the best course of action, I cannot think of anything else to try at this point.

I guess we can close this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T12:01:10Z

Thanks for the summary. 

Regarding NProcs 2 vs. 4, the performance differences aren't big, and are not very consistent. However, I'd prefer to keep it as 4 since higher parallelism might be helpful when we have more tests in the future, and may help us to expose flakes (similar effect as --race).

Regarding the `--race` flag, it helps us to detect flakes, and we have a couple of those, so it is worth using it even at the cost of 2min. 

I think what could make sense is to drop this flag for presubmits, and only use it for periodic tests. Ideally, local runs also enable the flag by default. WDYT @tenzen-y @alculquicondor @trasc ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T12:22:42Z

I also think it would make sense to have a generic env. var like PRESUBMIT, and based on it control the optimizations like INTEGRATION_RACE=false, or INEGRATION_RUN_ALL=false (or directly set the INTEGRATION_TEST_FILTERS). Then, if we change our decisions about presubmit config we don't need to update two places. WDYT?

### Comment by [@trasc](https://github.com/trasc) — 2024-10-02T12:45:27Z

> I think what could make sense is to drop this flag for presubmits, and only use it for periodic tests. Ideally, local runs also enable the flag by default. WDYT @tenzen-y @alculquicondor @trasc ?

Even the race detection might be sometimes flaky for some parts of the code, maybe due to some unfortunate test ordering, I still think it's better to continue doing the check in presubmit.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-02T15:10:45Z

> I think what could make sense is to drop this flag for presubmits, and only use it for periodic tests. Ideally, local runs also enable the flag by default. WDYT @tenzen-y @alculquicondor @trasc ?

Before we enable the race detection, there are many race issues in our integration testing: https://github.com/kubernetes-sigs/kueue/pull/2468

So, I'm suspecting that the periodic bot often fail by race issue once we diable it in the presubmit.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-02T18:40:55Z

> I think what could make sense is to drop this flag for presubmits, and only use it for periodic tests. 

I would not do that. When a race makes it to the main branch, it becomes our problem to solve. The contributor that introduced the change, unfortunately, might not be available.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T05:56:45Z

Ok, thank you for the input, we have a consensus here. 

/close 
Thank you for the work on the issue, the gain is great. Feel free to submit follow up PRs or open issues if you have more ideas for improvement.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-03T05:56:49Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2993#issuecomment-2390584814):

>Ok, thank you for the input, we have a consensus here. 
>
>/close 
>Thank you for the work on the issue, the gain is great. Feel free to submit follow up PRs or open issues if you have more ideas for improvement.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
