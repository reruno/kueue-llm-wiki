# Issue #5166: revisit building power/s390x?

**Summary**: revisit building power/s390x?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5166

**Last updated**: 2025-09-28T17:59:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-05-05T20:14:36Z
- **Updated**: 2025-09-28T17:59:22Z
- **Closed**: 2025-09-28T17:58:52Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 22

## Description

https://github.com/kubernetes/kubernetes/issues/131555

Kubernetes has been discussing supporting 390x and PowerPC over the last few months.

Is there any reason why Kueue builds these images? 


https://github.com/kubernetes-sigs/kueue/blob/3d4725b8553082570b86ad7b81120570c26ea5fa/Makefile#L29

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T05:58:44Z

IIRC, that has no specific reason. I'm ok with removing it.
However, let me know what you think, IBM folks. > @dgrove-oss @tardieu

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T06:34:23Z

It seems that these platforms are also being used: https://github.com/kubernetes-sigs/kueue/pull/1956.

cc: @satyamg1620

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-06T12:56:34Z

I think we should follow what upstream Kubernetes does.  It looks fairly certain it will drop the builds and we should be consistent with that.

### Comment by [@satyamg1620](https://github.com/satyamg1620) — 2025-05-06T13:09:11Z

@mbobrovskyi ,s390x and power platforms are also being used.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T13:49:14Z

> [@mbobrovskyi](https://github.com/mbobrovskyi) ,s390x and power platforms are also being used.

Thank you for the confirmation!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:07:51Z

@kannon92 Do you still think that we should drop the power/s390x building? IIUC, k/k will drop the support due to too much maintenance costs. However, in Kueue, we support those architectures as a soft, which means we do not perform E2E testing for those platforms. We just built the images for those.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-07T15:10:52Z

> [@kannon92](https://github.com/kannon92) Do you still think that we should drop the power/s390x building? IIUC, k/k will drop the support due to too much maintenance costs. However, in Kueue, we support those architectures as a soft, which means we do not perform E2E testing for those platforms. We just built the images for those.

It bothers me that we release these images but not test them?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-07T15:11:54Z

I think its fine to keep them but I'm unclear on what our stance on support is for this.

If any bugs are reported, do we claim to support/fix these architectures?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:16:46Z

> I think its fine to keep them but I'm unclear on what our stance on support is for this.
> 
> If any bugs are reported, do we claim to support/fix these architectures?

I think we probably face the problem after k/k stops supporting Power PC, since I guess the future k/k codes will have non incompatible codes with Power PC. If Kueue uses those codes as a library, we probably face the issue for power PC.

The key point is which levels should we support for the problems. This is actually an OSS project. So if anyone does not provide any bug fixes, those will never be fixed.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-08T02:45:51Z

I chatted with @BenTheElder about this offline. I think Kueue can consider to support power/s390x even if Kubernetes drops support.

It is really up to Kueue project to support or not.

@satyamg1620 mentions these are used so I am inclined to keep the builds. The only downside of this is that it makes our build/push pipelines a lot slower.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-08T04:15:15Z

> @satyamg1620 mentions these are used so I am inclined to keep the builds. The only downside of this is that it makes our build/push pipelines a lot slower.

Yeah, that is another drawback. I'm ok with soft supporting if @satyamg1620 uses it in their platform.
However, when we face any problems for the platform, we might remove it.

@mimowo Any thoughts?

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-05-08T05:18:14Z

Your build times feel fast relative to kubernetes/kubernetes :-)

10m is roughly building a kubernetes/kubernetes release just for amd64 on an amd64 host.
10m here seems to get us all platforms even with modest machine sizes.

For local development I would suggest maybe the makefile can be reworked to conveniently build for just the host platform, you almost have that with the kind target currently. https://github.com/kubernetes-sigs/kueue/pull/5193

### Comment by [@dilipgb](https://github.com/dilipgb) — 2025-05-09T05:46:32Z

@BenTheElder @tenzen-y @kannon92 here are some of my thoughts on building the s390x images for kueue.

1. Currently build time for multiarch using docker buildx in emulation mode is taking approximately 10 minutes on s390x and 20 minutes to complete build using docker buildx on x86. 
2. I agree with @BenTheElder suggestion of having native build for host platform and then another block for mutiarch in the Makefile. 
3. We can run multiarch in the nightly jobs and host platform build on each PR. Any issues related to secondary architecture builds like s390x, arm, ppc64le which can be fixed based on the nightly job status and will not block the PR. (Just a thought, we can discuss on potential issues you may foresee with this approach.)
4. We can use multiarch build on release branch and during the release cut by conditionally executing the workflow. Similar approach we implemented for buildpacks lifecycle project (https://github.com/buildpacks/lifecycle/blob/main/.github/workflows/test-s390x.yml)
5. Running the tests can be performed nightly for s390x and we can fix the issues without blocking any PRs. In case any specific feature implementations to s390x can be verified by manually triggering the workflow.

Our team is committed to maintain the CI and keep it green and fix any issue that arises in the build/test process. I'm happy to know your thoughts on this proposal.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-09T05:58:53Z

The proposal sounds great to me. We will have faster presubmit PR builds, and at the same time continue to release the images for the architecture in the foreseeable future, plus test on nightly. cc @tenzen-y 

Given the nature of the kueue project, which is relatively high level I don't expect any problems specific to architectures, and don't remember any from the past. Still keeping the nightly build on all architectures is a good sanity check before release. we certainly don't need building all archs on every PR presubmit

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T14:19:27Z

> The proposal sounds great to me. We will have faster presubmit PR builds, and at the same time continue to release the images for the architecture in the foreseeable future, plus test on nightly. cc [@tenzen-y](https://github.com/tenzen-y)
> 
> Given the nature of the kueue project, which is relatively high level I don't expect any problems specific to architectures, and don't remember any from the past. Still keeping the nightly build on all architectures is a good sanity check before release. we certainly don't need building all archs on every PR presubmit

Does `nightly` mean periodic prow CI? If yes, I'm fine with the idea. The periodic CI job is a better way of failure tracking.

### Comment by [@dilipgb](https://github.com/dilipgb) — 2025-05-12T14:26:05Z

> Does nightly mean periodic prow CI? If yes, I'm fine with the idea. The periodic CI job is a better way of failure tracking.

Yes. A scheduled Job executed everyday on prow CI.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-10T14:51:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T07:50:51Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T08:08:15Z

I merged the first PR towards this, but it causes failures: https://github.com/kubernetes-sigs/kueue/issues/6517

Maybe it is better to revert and first prepare all steps, including (4.), to make sure we continue releasing the custom architecture images.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-28T17:58:47Z

I think we can close this.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-28T17:58:53Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5166#issuecomment-3344009335):

>I think we can close this.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-28T17:59:22Z

We are keeping these builds and some refactorings were made to speed this up.
