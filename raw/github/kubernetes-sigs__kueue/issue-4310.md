# Issue #4310: Allow publishing Kueue images prior to merge to the main branch

**Summary**: Allow publishing Kueue images prior to merge to the main branch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4310

**Last updated**: 2025-05-09T16:26:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-19T09:52:15Z
- **Updated**: 2025-05-09T16:26:07Z
- **Closed**: 2025-05-09T16:25:27Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 24

## Description

**What would you like to be added**:

I would like to be able to push some images prior to the publication to the main branch.

We certainly don't want to push all branches, so I would propose to modify the rules for publishing [here](https://github.com/kubernetes/test-infra/blob/dfef626025f921e6769f3a355f5ee38570d80b1d/config/jobs/image-pushing/k8s-staging-kueue.yaml#L8-L12) using a dedicated entry "^push-prototype-". Users who would want to push their branches would use this prefix to their branch names.

Actually, there is already a workaround by naming the branch with the `release-` prefix, but it does not capture the intention.

**Why is this needed**:

To be able to hand an image to a user for testing. 

This is inspired by discussions around https://github.com/kubernetes-sigs/kueue/pull/4165, but there are other cases where we have a "design partner" and being able to share them an image from branch would be great.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T09:52:37Z

cc @tenzen-y @gabesaba @dgrove-oss @BenTheElder wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T09:55:39Z

Actually, I just realized, looking at the rules, there is already a workaround by naming the branch with the release- prefix, but it does not capture the intention, and I believe this is a valid use-case, not something we need to be "securing" by obfuscation :)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T09:56:22Z

cc @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T11:26:35Z

Could we prepare a separate dedicated dir or tag prefix something like pre-${IMAGE_HASH}? Because in general, the latest image is recognized as the main branch (merged) image.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T12:34:00Z

This would be ideal, but not sure how much work this would be. Maybe an acceptable solution which is "in the middle" is to don't push such images with the "latest" tag.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T07:58:08Z

@tenzen-y actually, we are not using the "latest" tag, and our installation guide only relies on "main", as per https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version and https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/kustomization.yaml#L17.
 So, I think it is safe to publish the branch images from selected branches under kueue/kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:34:18Z

> [@tenzen-y](https://github.com/tenzen-y) actually, we are not using the "latest" tag, and our installation guide only relies on "main", as per https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version and https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/kustomization.yaml#L17. So, I think it is safe to publish the branch images from selected branches under kueue/kueue.

The "latest" is reserved tag by OCI. If we do not specify any tag, the "latest" is automatically picked up and downloaded.
I think shipping the non-merged images as "latest" is pretty aggressive.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T19:17:09Z

It seems that technically `latest` is an image tag like any other. 

For example:
```
> docker pull registry.k8s.io/kueue/kueue:latest 
Error response from daemon: manifest for registry.k8s.io/kueue/kueue:latest not found: manifest unknown: Failed to fetch "latest"
```
```
> docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:latest   
Error response from daemon: manifest for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:latest not found: manifest unknown: Failed to fetch "latest"
```
```
> docker pull kindest/node:latest
Error response from daemon: manifest for kindest/node:latest not found: manifest unknown: manifest unknown
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T14:07:41Z

I have synced on this with @tenzen-y , and we would like to run the following pilot process which can be adjusted as we collect feedback.
1. An eligible contributor (mentioned as reviewer or approver in any OWNERS file) opens a PR in Kueue against the main branch and asks as to enable staging repo pushes (either on priv or on the PR itself)
2. A maintainer (who has admin permissions to the Kueue repo) evaluates the request and creates manually a branch named “staging-push-{pr number}”
3. The maintainer cherry-picks the PR onto the branch manually (or the contributor opens another PR which is merged)
4. After the original PR is closed (merged to main or cancelled), maintainers can delete the branch

cc @gabesaba @PBundyra @dgrove-oss @kannon92 @mbobrovskyi wdyt?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-27T14:12:01Z

This could work but I think #sigs-k8s-infra input on this should be given. (cc @BenTheElder @upodroid )

If someone really wants to test an image, they can also take the branch and publish those images to a non k8s-repo and have people test that.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-27T14:13:49Z

> I have synced on this with @tenzen-y , and we would like to run the following pilot process which can be adjusted as we collect feedback.

Lgtm

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-27T14:16:45Z

Seems plausible to me.  Would we also delete the image when we delete the branch?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T14:17:07Z

> If someone really wants to test an image, they can also take the branch and publish those images to a non k8s-repo and have people test that.

Sure, the idea is to allow all owners to do so via legit way, without the need to publish to dockerhub, or public cloud-provider specific registeries

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T14:17:51Z

> Seems plausible to me. Would we also delete the image when we delete the branch?

I think no need to, the images are only push to staging, which has retention period of 90 days. After that, the images will be deleted automatically.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T14:21:14Z

> This could work but I think #sigs-k8s-infra input on this should be given. (cc @BenTheElder @upodroid )

Yes, to make this work we will need to adjust test-infra registry [section](https://github.com/kubernetes/test-infra/blob/dfef626025f921e6769f3a355f5ee38570d80b1d/config/jobs/image-pushing/k8s-staging-kueue.yaml#L8-L12) by adding `^staging-push-". Trying to see here first if this idea gets support, which we could use to support the PR in test-infra.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-03-27T17:13:40Z

We generally don't consider this best practice, because then a PR run could push an image to staging that overwrites a tag you planned to promote to prod, and few people actually reliably vet the images they promote, instead copying the current digest of the tag right at promotion time, and PR runs can exfiltrate any secrets you may have in the cloud build project.

Have you considered a secondary branch? Or pushing images to your own unofficial location?

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-03-27T17:15:10Z

Also, currently, the "trusted" cluster with access launch to the cloud builds is prohibit from running _any_ presubmits, because PR testing is such a security footgun. This cluster intentionally has very limited scope, a small set of approvers, and basically only allows the templated cloudbuild triggering jobs.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-03-27T17:34:29Z

> Sure, the idea is to allow all owners to do so via legit way, without the need to publish to dockerhub, or public cloud-provider specific registeries

Right, if these are *pre-merge* then surely they're not official?

Also can't you share code and let fellow maintainers build locally, or use a shared development branch?

> Sure, the idea is to allow all owners to do so via legit way, without the need to publish to dockerhub, or public cloud-provider specific registeries

... the staging repos are still public cloud-provider specific, and they're meant to be an implementation detail of publishing to registry.k8s.io, NOT consumed by users. registry.k8s.io is how we serve images to users.

The docs at https://registry.k8s.io has more about how we shape traffic / control costs (primarily by serving same-cloud, same-region)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T18:08:46Z

@BenTheElder thank you for the responses, I see your concerns and it probably means we need to abandon the idea. 

>  because then a PR run could push an image to staging that overwrites a tag you planned to promote to prod

Good point, this is subtle, I haven't thought about it. The image tag is controlled by Kueue [Makefile](https://github.com/kubernetes-sigs/kueue/blob/main/Makefile). I think currently it would not overwite, but it could be a point of risk for the future changes in the Makefile.

> Have you considered a secondary branch?

What do you mean by secondary branch? In the proposal in https://github.com/kubernetes-sigs/kueue/issues/4310#issuecomment-2758190343 we consider creating "staging-push-{PR_number}" branches manually in kueue repo, just for this purpose. So, maybe this is a generalization of the "secondary branch" idea?

>  Or pushing images to your own unofficial location?

Yes, I've seen people pushing to priv/public dockerhub locations, or their cloud-provider registries. Still this sounds like a workaround rather than a proper alternative. Still, it  does not require any changes in the process.

> Also can't you share code and let fellow maintainers build locally, or use a shared development branch?

The motivation is to allow sharing the image easily with users who are willing to test code in their environment. Some environments are hard to replicate by developers. For example, due to scale or workload characteristics, machines used, etc.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-03-28T01:37:17Z

> Good point, this is subtle, I haven't thought about it. The image tag is controlled by Kueue [Makefile](https://github.com/kubernetes-sigs/kueue/blob/main/Makefile). I think currently it would not overwite, but it could be a point of risk for the future changes in the Makefile.

If you push images from PRs, I can send a PR that pushes arbitrary tags, the build is just more code. I can also attempt to dump creds to the logs.

We have a mitigation of not immediately running jobs for unknown users, but it's not that hard to get an org member account.

Ideally people are tracing promotion PR digests to post-merge build logs, but often they aren't.

> What do you mean by secondary branch? In the proposal in https://github.com/kubernetes-sigs/kueue/issues/4310#issuecomment-2758190343 we consider creating "staging-push-{PR_number}" branches manually in kueue repo, just for this purpose. So, maybe this is a generalization of the "secondary branch" idea?

Kubernetes has experimented with "feature branches" before, which aren't releases, but are upstream.

It had a lot of pitfalls, but so does any variation on upstream but not quite official yet.

> Yes, I've seen people pushing to priv/public dockerhub locations, or their cloud-provider registries. Still this sounds like a workaround rather than a proper alternative. Still, it does not require any changes in the process.

Well ... kubernetes I would say handles this via alpha features, which are not guaranteed yet, but are mainline.

"officially hosted but not actually merged yet" builds is a workaround IMHO.

> The motivation is to allow sharing the image easily with users who are willing to test code in their environment. Some environments are hard to replicate by developers. For example, due to scale or workload characteristics, machines used, etc.

I meant can they build the image locally? We can also probably make that easier / faster.

Is testing in these environments blocking merges? That doesn't sound terribly reasonable. If I send a PR do I have to wait for some manual third party testing to occur?

If they're proposed features, feature gates + alphas?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-28T02:02:08Z

Could we do something like a trusted presubmits that publishes the PR to staging?

Thinking more like a presubmits that is restricted to reviewers/maintainers of Kueue that would publish an image on a PR..

So we could trigger a push on a PR but only allow it for a small subset of org members.

### Comment by [@BenTheElder](https://github.com/BenTheElder) — 2025-03-28T03:08:24Z

RE: restricted presubmit triggering — That's an open feature request to prow, though the use case was scale tests (so preventing DoW / abuse, not securing release infrastructure). That functionality doesn't exist currently and the prow maintainers have been stretched pretty thin. The CI needs more maintainers for upkeep of the existing feature set. (I steppped down there years back to work on other things myself ...)

Even if we had restricted triggering though, again, we've seriously discussed disabling public read for staging registries, traffic costs have obliterated the project's budget before to the tune of millions annually, we very intentionally do not point external traffic directly at anything other than project controlled domains where we can load shift and cost engineer immediately as needed.
Staging doesn't directly have that because it's supposed to be an implementation detail of publishing to registry.k8s.io

One other suggestion I had was ghcr.io on the personal forks for unofficially sharing unmerged images, but we're not sure if that works yet. If it does that might be a reasonable ~universally available alternative to publish prototype builds.

Feature gated code is my other suggestion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-09T16:25:22Z

/close 
FYI: https://github.com/kubernetes/test-infra/pull/34748

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-09T16:25:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4310#issuecomment-2867155189):

>/close 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
