# Issue #3588: Document Support Policy on Kueue Releases

**Summary**: Document Support Policy on Kueue Releases

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3588

**Last updated**: 2025-01-27T09:15:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-11-18T17:57:35Z
- **Updated**: 2025-01-27T09:15:29Z
- **Closed**: 2025-01-27T09:05:27Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 8

## Description

As Kueue matures, there is some questions on when Kueue decides that a release is no longer supported. I don't really know when we decide a release is no longer in support. 

My hope would be some kind of documented policy on when we stop maintaining release branches and force people to use later versions.

```[tasklist]
### Tasks
- [ ] https://github.com/kubernetes/test-infra/pull/33833
- [ ] https://github.com/kubernetes/test-infra/pull/33899
- [ ] Document Release Policy
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T18:13:15Z

cc @mwielgus @tenzen-y @mwysokin @dgrove-oss 

Good question, I think we generally support only the last released version, but not sure this is documented anywhere. 

It may also be a bit tricky to set rigid rules because the release cadence isn't as fixed. In the past we had 1 to 4 months intervals between releases, which could be making some difference also.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-18T18:22:53Z

One rough proposal I talked with @tenzen-y about is maybe linking support to the k8s release version the APIs are based on. This does mean that we are supporting much longer release branches. Generally Kueue is pretty good about upgrading the k8s dependencies once the newest patch of the latest version is released (ie 1.32.1, we upgrade k8s release. Maybe that can be a release?).

For openshift, we offer LTS on k8s release branches and eventually we will end up not being able to support certain kueue releases as the skew increases but I think LTS for Kueue may be linked with the k8s version eventually. I would see folks wanting to run/support Kueue on 1.28 as long as 1.28 is still in support. It isn't clear to me what Kueue release we would support in this case.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-21T17:39:59Z

Summarizing my input from the wg call today.  Wearing my "consumer of Kueue" hat,  the minimum expectation would be that at some point relatively soon we'd get into a steady state where there would always be a release of Kueue that is supported by this community that would work with each version of Kubernetes that is being supported by the Kubernetes community. 

This doesn't mean that as a consumer of Kueue I expect the Kueue community to support every Kueue release on every supported version of Kubernetes.  What I do expect is:
1. There is some well-defined structure of Kueue release streams (eg, fast and stable).  Not every Kueue release needs to be a stable release. 
2. The stable stream would have always a release that is supported by the Kueue community on each version of Kubernetes that is supported by the Kubernetes community.
3. If a cluster is running a supported version of Kubernetes, then the Kueue community supports upgrading Kueue "in place" on that cluster from the Nth to N+1 release in Kueue's stable release stream.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-22T17:48:20Z

Floating this idea with @mrunalp, we are happy with @dgrove-oss's proposal.

I would go a little farther and ask for a formal commitment for n and n - 1 support. And to me, I think that means we should make sure we have periodic tests that verify that n and n - 1 run on supported versions of Kubernetes. I'm happy to help here on the release side. I opened up https://github.com/kubernetes/test-infra/pull/33833 as one option for how this would look in practice.

We will need to revisit this once Kueue hits GA but until that time, I think n and n - 1 support would be sufficient.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-03T20:59:55Z

Given that @mimowo approved https://github.com/kubernetes/test-infra/pull/33833, should we consider a policy of supporting two releases of Kueue and make sure that periodics cover this?

If so, I can add some text to kueue's site stating this.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T09:30:12Z

I wouldn't jump to this conclusion yet. For now, we only support the last release. For the last release we try to basically backport all bugfixes. 

For the one-before release we sometimes make releases, so I'm ok with the infra test, but cherry-picking to this branch is best effort only, so I wouldn't like to call it supported officially yet, until we agree what it entails. 

In fact, most bugfixes are not backported to the one-before,. We often have complications backporting to the last release, so backporting one more is extra investment - we need to chase people to prepare the cherry-picks, and guide how to do it when there are numerous conflicts.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-04T19:36:47Z

> I wouldn't jump to this conclusion yet. For now, we only support the last release. For the last release we try to basically backport all bugfixes.
> 
> For the one-before release we sometimes make releases, so I'm ok with the infra test, but cherry-picking to this branch is best effort only, so I wouldn't like to call it supported officially yet, until we agree what it entails.
> 
> In fact, most bugfixes are not backported to the one-before,. We often have complications backporting to the last release, so backporting one more is extra investment - we need to chase people to prepare the cherry-picks, and guide how to do it when there are numerous conflicts.

+1
The release branch management is a hard thing, as I told at the last KubeCon you.
So, considering the Kueue development activity (it means that Kueue is very aggressive and actively developing projects), guaranteeing the patch release is challenging.
As you know, we need to maintain the release notes, code conflicts, and feature gates between the main and release branches.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T09:15:09Z

FYI I merged the PR with the new release scheme, the tentative schedule for the next couple of releases:

<b style="font-weight:normal;" id="docs-internal-guid-c312edd3-7fff-1f72-8039-ad91f0bbe991"><div dir="ltr" style="margin-left:0pt;" align="left">
Kueue | Target release date | Aiming to compile against
-- | -- | --
0.11 | 17th March 2025 | 1.32.x
0.12 | 19th May 2025 | 1.33.1
0.13 | 14th July 2025 | 1.33.x
0.14 | 15th September 2025 | 1.34.1
0.15 | 17th November 2025 | 1.34.x
0.16 | 18th January 2026 | 1.35.1

</div></b>
