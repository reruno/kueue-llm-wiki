# Issue #3090: Add the reason why my Jobs are infinity restarting to troubleshooting guide

**Summary**: Add the reason why my Jobs are infinity restarting to troubleshooting guide

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3090

**Last updated**: 2025-12-25T08:05:16Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-09-18T17:08:03Z
- **Updated**: 2025-12-25T08:05:16Z
- **Closed**: 2025-12-25T08:05:15Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 23

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to add hints to investigate the reason why my jobs are restarting at infinity.

**Why is this needed**:
The production cluster has many OSS and non-OSS controllers and webhook servers.
Recently, I faced very strange Job restarting problems caused by the collaboration with Kueue and other webhook servers.
Let me explain step by step what happened:

1. Batch User: Submit a Pod to the cluster.
2. Webhook X: Insert credentials to Pod based on Pod creation event.
3. Kueue: Gating the Pod and create the corresponding Workload.
4. Kueue: Admit the Pod and ungating the Pod.
5. Webhook X: Try to insert credentials to Pod based on Pod updating event . Here, webhook X accidentally drops some fields from the PodSpec due to the older kube client version.
6. Kueue: Detect the PodSpec changes based on https://github.com/kubernetes-sigs/kueue/blob/b9e173091c53456ae6858d9a10de81e6ba07ec62/pkg/util/equality/podset.go#L29-L37
7. Kueue: Stop the Pod due to missing the corresponding Workload like the following:

```shell
0s          Normal    CreatedWorkload       pod/xxx                                                        Created Workload: yyy/xxx
0s          Normal    QuotaReserved         workload/xxx                                                   Quota reserved in ClusterQueue zzz, wait time since queued was 1s
0s          Normal    Admitted              workload/xxx                                                   Admitted by ClusterQueue zzz, wait time since reservation was 0s
0s          Normal    Scheduled             pod/xxx                                                        Successfully assigned yyy/xxx to nnn
0s          Normal    Stopped               pod/xxx                                                        No matching Workload; restoring pod templates according to existent Workload
```

8. Kueue: Recreate the Workload corresponding to the Pod
9. Go to step 2, and looping.

The root cause was that webhook X used a slightly older kube client (in my case 1.23). But, I think that this could happen in situations where the cluster version is Kueue minimum required version, webhook X uses the Kueue minimum required version kube client, and the latest version of Kueue is installed.

Additionally, I can imagine that the Pod integration has a chance to encounter this problem, mostly since the cluster often has some webhook servers to insert cluster-specific credentials, volumes, and configs.

Although I consider some solution to address this problems like the following, all approaches have disadvantages. So, I would proposes to just add a troubleshooting guide.

- Strictly checking PodSpec differences instead of comparing a whole of PodSpec there: https://github.com/kubernetes-sigs/kueue/blob/b9e173091c53456ae6858d9a10de81e6ba07ec62/pkg/util/equality/podset.go#L29-L37
  - Disadvantage: This can not detect the dropped fields by external components.
- Considering the cluster version when comparing the PodSpec.
  - Disadvantage: This may bring additional computation and decrease admission throughput.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T17:09:56Z

@alculquicondor @mimowo, please let me know what you think.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-18T17:25:52Z

Ah, the good ol' webhooks!

We have encountered a set of problems with webhooks too. They typically cause problems when they do mutations during Pod updates. I'd be happy to review a doc, although I'm not sure how generically useful we can make it. They are likely to be obscure bugs most of the times.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T17:31:36Z

> Ah, the good ol' webhooks!

I guess that such webhooks are running In typically long-running clusters :( Actually, my cluster was launched 5 years ago lol

> although I'm not sure how generically useful we can make it. They are likely to be obscure bugs most of the times.

Yeah, indeed, that was my hesitation whether or not we should add the document to this repository...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T17:41:06Z

Maybe, we can generalize and say the following:

When you observe the infinity of Job admission and requeuing, you can check if there are any webhooks to mutate Pods triggered by Pods update event. Such webhook sometimes leads to differences between admitted Pod and deployed Pod, and then the Kueue missing the exact Workload and Pod combination.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-09-18T17:44:37Z

We encountered a similar infinite loop in the process of developing AppWrappers and using them to wrap RayClusters.   The test of deep semantic equality applied in `equality.comparePodTemplate` as invoked from `jobframework.equivalentToWorkload` was also the sticking point. 

In our case, there were no webhooks involved. The issue was that our implementation of `GenericJob.PodSets()` built the PodSets by using Unstructured to parse the `runtime.RawExtension`.  This doesn't cause the non-zero default values to be filled in.  In particular, there was a container Port with an unspecified Protocol (which defaults to `TCP`).   This PodSet would then always fail an equality test with the PodSet in the Workload object, since the PodSpecTemplate in the Workload object would have made a round trip to the API server and the default values got filled in. 

We worked around this by doing a custom selective copy of information from the PodSpecTemplate built by Unstructured (after first attempting to try to use `Scheme.Default` which didn't work because it isn't properly initialized when importing just the api).

Is a deep equality of PodSpec really required?   Could a more selective function that only looked at a subset of the PodSpec that was relevant to scheduling be used instead?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-18T17:51:46Z

> Is a deep equality of PodSpec really required? Could a more selective function that only looked at a subset of the PodSpec that was relevant to scheduling be used instead?

That's something that can be considered. For the most part, we care about resource requests, node selectors and tolerations.
But the landscape could change. DRA fields are probably the next thing to watch for on the horizon.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T13:06:52Z

> Strictly checking PodSpec differences instead of comparing a whole of PodSpec there

Actually, I evaluated the comparing only scheduling directives when I faced this issue. But, as I and Aldo mentiond, the approach has some disadvantages, specifically, new future scheduling directives. So, I would not like to introduce strictly only the comparison of scheduling directives for now.

But, I gues that we may want to reevaluate the solution in the future.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-09-19T13:24:28Z

I think it's a tradeoff of non-ideal solutions.  A selective equality test has to be updated within Kueue each time there is a new addition to the PodSpec that Kueue is interested in.  A non-selective equality test has been shown to have recurring problems interacting with other components that mutate PodSpecs and have older definitions of the type.   

My instinct is that the first (selective test) is less error-prone overall, mainly because it is entirely contained within Kueue and there is a clear point to check/update it (when Kueue updates its Kubernetes version dependency and there is a new field we care about, the equality function is updated).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T13:31:42Z

Yeah, I agree with @dgrove-oss

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T21:09:54Z

> I think it's a tradeoff of non-ideal solutions. A selective equality test has to be updated within Kueue each time there is a new addition to the PodSpec that Kueue is interested in. A non-selective equality test has been shown to have recurring problems interacting with other components that mutate PodSpecs and have older definitions of the type.
> 
> My instinct is that the first (selective test) is less error-prone overall, mainly because it is entirely contained within Kueue and there is a clear point to check/update it (when Kueue updates its Kubernetes version dependency and there is a new field we care about, the equality function is updated).

Your claim sounds reasonable. But, I'm wondering if we should compare image, volume, and some other fields, not only scheduling directives since we should trigger reconciliation based on the PodSpec modifications.

So, I would propose to summarize the fields that we need to care modifications before we move this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T21:11:38Z

However, I think that evaluating the selective test factors is out of the scope of this issue.
So, I will try to create a dedicated one.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T21:20:00Z

> However, I think that evaluating the selective test factors is out of the scope of this issue. So, I will try to create a dedicated one.

Opened: #3103

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-18T21:29:49Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-18T23:12:14Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-18T23:41:47Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-18T00:36:39Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-29T05:42:43Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-28T05:58:52Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T06:13:36Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-26T06:50:31Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-25T07:46:20Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-25T08:05:10Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-25T08:05:16Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3090#issuecomment-3691110597):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
