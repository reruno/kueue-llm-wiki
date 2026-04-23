# Issue #8858: WAS integration: run e2e tests using "main" kubernetes to proactively ensure compatibility

**Summary**: WAS integration: run e2e tests using "main" kubernetes to proactively ensure compatibility

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8858

**Last updated**: 2026-02-06T10:43:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-28T14:51:23Z
- **Updated**: 2026-02-06T10:43:25Z
- **Closed**: 2026-02-06T10:43:24Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 21

## Description

**What would you like to be added**:

With the ongoing work in kubernetes on WAS https://github.com/kubernetes/enhancements/tree/master/keps/sig-scheduling/4671-gang-scheduling there is some risk for incompatibility. 

I imagine a dedicated CI job which runs periodically every day. Our alerting will tell us if the compatibility is broken.

**Why is this needed**:

In that case we should know early, before k8s is released, so that we can adjust Kueue, or flag early the compatibility problems.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T14:51:48Z

cc @tenzen-y @gabesaba @mbobrovskyi @sohankunkerkar @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T14:54:52Z

I would probably not suggest this.

But we could consider a dedicated job with WAS enabled on kind clusters (1.35 and on).

But honestly we haven't discussed the impact of WAS on Kueue.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T14:55:53Z

Right now, in 1.36 we _may_ get Job gang scheduling. But there is so much in flight.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T15:13:53Z

> I would probably not suggest this.

Why?

> But we could consider a dedicated job with WAS enabled on kind clusters (1.35 and on).

IIUC currently 1.35 WAS is alpha only, so I think it is not that relevant. It becomes onteresting on "main".

We could certainly have two jobs:
- "main" with WAS enabled
- "1.36" with WAS enabled

But it feels "main" is more important to get early feedback about incompatibilities.

> But honestly we haven't discussed the impact of WAS on Kueue.

I'm actually part of some internal discussions currently, but the integration is certainly coming.

Discussions are ongoing, but no "dry" discussion can replace actual testing IMO. Even if we discuss and conclude "no impact", the impact might be, and test can help us to spot the issues early.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T15:39:27Z

> Why

What do we do if kubernetes main is breaking? Should we do local-up-cluster or kind builds? I guess we could make the job informing and monitor it but not block. But someone has to sign up to maintain this job and make sure things keep running.

Its a pretty large cost to maintain main branches.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T15:45:03Z

> What do we do if kubernetes main is breaking? Should we do local-up-cluster or kind builds? I guess we could make the job informing and monitor it but not block.

Yes, that was my plan, just make it informative periodic build.

> Its a pretty large cost to maintain main branches.

I'm not sure I understand what you mean here. It wouldn't be the cost on Kueue maintainers, but we could open issue in k8s core indicating that some changes are breaking compatibility.

We could also then know early we need to change Kueue.

There is also some cost for Kueue if new kubernetes is released and Kueue is not compatible, and we need 1 month to adapt.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T17:10:53Z

> I'm not sure I understand what you mean here. It wouldn't be the cost on Kueue maintainers, but we could open issue in k8s core indicating that some changes are breaking compatibility.

I was thinking Kueue team needs to maintain a way to build kubernetes main without bringing that in as a go.mod dependency and continue to maintain that code.

Maybe @aojea, @pohly or @BenTheElder have established patterns for this for kubernetes sig projects?

I'd love to have kubernetes-sig dogfood features so I am supportive of the idea. Just trying to understand how much effort we want to maintain.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T17:57:45Z

I think that this is very helpful for both Kueue and kube-scheduler since 2 primary reasons.
The first is, as @mimowo mentioned, that the Kueue side could detect the scheduler-side bugs immediately, and then the scheduler side can fix that before release. 

The second is that the Kueue side reports the incompatible and irreversible scheduler-side changes. For example, when scheduler-side introduced API fields incompatible with Kueue accidentally, Kueue side can find that and block releasing the incompatible ones or proposing mitigation ways to kube-scheduler side.

For the actual setup solution, I guess that we can build a KinD node image with https://kind.sigs.k8s.io/docs/user/quick-start/#building-images, but I'm not sure if this way truly works well.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T21:09:52Z

> I'm actually part of some internal discussions currently, but the integration is certainly coming.

I know that @sohankunkerkar and I are very interested in this so I hope this integration could be community led at some point.

My goal now is to review KEPs from k/k and think about impacts to Kueue. And try and think through how workloads will leverage WAS so we can eventually think more about it for Kueue.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-28T21:29:47Z

+1 on having early visibility into WAS compatibility. For the CI approach, I think building KinD images from k/k main is the right path.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2026-01-28T22:41:51Z

> I was thinking Kueue team needs to maintain a way to build kubernetes main without bringing that in as a go.mod dependency and continue to maintain that code.

I'm not aware of any sigs projects that *import* staging modules or similar from main. 
(And again, if you speak to sig arch / code organization subproject ... importing k/k aside from staging is NOT supported ...)

Most SIGs subprojects are running with stable releases and relying on the fact that we normally have skew support (e.g. for client-go).
EDIT: The main exception being some tools that bring up clusters. But those are still importing stable packages/types, only using HEAD binaries.

If you just want to run Kubernetes/Kubernetes binaries from `main`, you can do that with various CI tools including `kind`, that's a very different problem that **shouldn't** have any relationship to your go.mod imports.

Keep in mind that you may need the absolute latest version of those tools, which themselves may have breaking changes from time to time. (e.g. https://github.com/kubernetes-sigs/kind/issues/3847)


> The second is that the Kueue side reports the incompatible and irreversible scheduler-side changes. For example, when scheduler-side introduced API fields incompatible with Kueue accidentally, Kueue side can find that and block releasing the incompatible ones or proposing mitigation ways to kube-scheduler side.

We usually handle this in k/k with something more like [apidiff](https://pkg.go.dev/golang.org/x/exp/apidiff) running in the main repo? There is a job checking this for client-go for example. We also have [a linter for the REST API types](https://github.com/kubernetes-sigs/kube-api-linter) for similar reasons + human review.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T23:01:12Z

@BenTheElder woukd there be any issue with having kind build node images on prow?

I know we hit Docker in docker but I guess we already support that.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2026-01-29T00:27:04Z

> @BenTheElder woukd there be any issue with having kind build node images on prow?

Running in prow is the main reason `kind` exists, actually, despite it having some challenges.

> I know we hit Docker in docker but I guess we already support that.

Yeah, the dind setup in test-infra is ... dubious (my doing many years ago ...), but it works OK for now and won't be unique to this repo.

We are building node images on every k/k PR.

However, I'd ask for this case that we use something like the `ci/latest` binaries to avoid unnecessarily re-compiling Kubernetes, as opposed to on a Kubernetes PR. 

Not all existing CI jobs have been ported to that, but new efforts should.

There are examples in test-infra, but basically this will work currently and is a lot cheaper than building Kubernetes from source:
```console
kind build node-image --type url https://dl.k8s.io/ci/$(curl -L https://dl.k8s.io/ci/latest.txt)/kubernetes-server-linux-$(go env GOARCH).tar.g
```

You can do some extra tricks to surface this version to testgrid, it's not super polished at the moment but doable (and not strictly necessary).

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2026-01-29T00:29:12Z

dl.k8s.io has various "marker files" for release branches (eg head of release-N, most recently tagged in release-N, ...), there are some docs in k/community or k/release IIRC.

ci/latest will be the most recent cross-compile of master, the layout of the folders is the same as tagged releases.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-29T01:28:00Z

Now that Ben has answered that this is possible to do and led us with many breadcrumbs (❤️ thank you!), we are left with how to best enforce that these tests could inform breakage in Kueue. I don't really think we have thought this through too much though.

From what I have seen with WAS most of the work is optional based on Workload/PodGroup API. There is hope to get this added into controllers in the future but I think the interaction is going to be quite pernicious and require careful thought.

One case is https://github.com/kubernetes/enhancements/pull/5711/changes#r2627477923.

If WAS introduces a workload premeption I don't quite understand how Kueue's workload priority class would play together. I don't expect any e2e tests to actually catch this unless we actually wrote them. I think catching integration issues may be best left to thinking through KEPS and calling out potential issues when you review.

For WAS I hope that a lot of the impact with Kueue (minus TAS) should be somewhat minimal because I hope that workload controllers would handle gang scheduling. And Kueue could just preempty the true workload (Job, JobSet, LWS) and the controller handles that.

### Comment by [@pohly](https://github.com/pohly) — 2026-01-29T09:51:04Z

> There are examples in test-infra

For example this one:

https://github.com/kubernetes/test-infra/blob/11704393c4d699555113c47cf52b64e6aa9b936e/config/jobs/kubernetes/sig-node/dra-ci.yaml#L38-L52

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T10:33:11Z

Thank you for the feedback!

Indeed so far Kueue relied on human review of changes in the core k8s, and we only reacted, and sometimes made small adjustments.

However, I think WAS is special, because:
1. WAS is a revolutionary and complex scheduling initiative in the core k8s (comparable to DRA) with many KEPs coming in. 
2. Integration of Kueue with WAS is one of our strategic goals
3. The feedback from Kueue is part of the requirements for WAS, so early feedback on the development phase is important. 
4. If some issues in the core API are overlooked it may result in the integration being deferred by months

In particular I foresee complexities around:
1. the TAS level when we start to use new algorithms for tighter integration
2. coordination of creating Workload API instances by custom (and built-in) controllers consistently with Kueue. Currently Kueue decides on the level of Workload by the "queue-name" annotation, but some of the decisions in the core or ecosystem I imagine could be breaking for Kueue, eg if k8s Job started to created Workload API by default, but Kueue's user wants to schedule at the JobSet level.

Given the subtle integration complexities I would like to support "human" review with also some automation for early testing. 

Certainly the tests would be "periodic" and only informative, so they would not block merging into Kueue. 

Also big thanks for exploring the technical aspects of how we could use "main" k8s for testing. This is invaluable as our expertise here is limited, so the guideline/hints can reduce the timeline significantly.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T13:45:20Z

/retitle WAS integration: run e2e tests using "main" kubernetes to proactively ensure compatibility

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-02T08:51:31Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-06T10:43:18Z

/close

Since https://github.com/kubernetes-sigs/kueue/pull/8935 and https://github.com/kubernetes/test-infra/pull/36359 have been merged.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-06T10:43:25Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8858#issuecomment-3859614896):

>/close
>
>Since https://github.com/kubernetes-sigs/kueue/pull/8935 and https://github.com/kubernetes/test-infra/pull/36359 have been merged.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
