# Issue #63: [Umbrella] ☂️ Requirements for release 0.1.0

**Summary**: [Umbrella] ☂️ Requirements for release 0.1.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/63

**Last updated**: 2022-04-12T17:17:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T16:38:51Z
- **Updated**: 2022-04-12T17:17:47Z
- **Closed**: 2022-04-12T17:17:46Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 35

## Description

Deadline: May 16th Kubecon EU


Issues that we need to complete to consider kueue ready for a first release:

- [x] Match workload affinities with flavors #3
- [x] Single heap per Capacity #87 
- [x] Consistent flavors in a cohort #59
- [x] Queue status #5
- [x] Capacity status #7 
- [x] Event for unschedulable workloads #91 
- [x] Capacity namespace selector #4
- [x] Efficient requeuing #8 
- [x] User guide #64
- [x] Publish image #52

Nice to have:

- [ ] Add borrowing weight #62
- [ ] E2E test #61
- [ ] Use kueue.sigs.k8s.io API group #23
- [ ] Support for one custom job #65

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T16:39:35Z

/kind feature

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T16:40:23Z

cc @ahg-g @ArangoGutierrez @denkensk thoughts? Did I miss something?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-24T16:43:15Z

Ohhhh that smell of a new release in the air.... uh lala

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-24T16:44:51Z

User guide is also needed.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-24T16:46:22Z

something we can quickly implement as well could be github-pages for small documentation? (I can volunteer have done that for other sigs)

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-24T16:47:39Z

#14 Is there any progress on this？ @ArangoGutierrez

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-24T16:57:28Z

we agree to wait for klog/v3 no? 

```
But this is changing soon https://github.com/kubernetes/enhancements/tree/master/keps/sig-instrumentation/3077-contextual-logging

In the meantime, if we stick with logr for now, I think it will be easier to switch to klog (v3?) once it supports contextual logging.
```

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-24T17:06:38Z

I would add https://github.com/kubernetes-sigs/kueue/issues/52 to that checklist

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-24T17:12:12Z

I don't think we should block the first release on https://github.com/kubernetes-sigs/kueue/issues/62, ceiling is workable for a 0.0.1 version .

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-24T17:43:53Z

can we set KubeCon EU as dead line for this? would be a nice thing to achieve

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-24T17:45:37Z

Yeah, I submitted a proposal to present it at KubeCon the general event, but will also be discussing it in the colo event.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-24T18:00:37Z

Great

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T19:06:37Z

I think we should be able to have something sooner. But kubecon EU is a nice hard deadline :) Added to the description.

> I don't think we should block the first release on #62, ceiling is workable for a 0.0.1 version .

I think it is indeed usable, but migrating to weights from the first version will avoid one breaking change. Sure... they are alpha APIs, but if we can avoid it, it would be great. Moved to nice-to-have.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-01T17:02:56Z

@alculquicondor can you pin this? so is easier to find

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T18:43:20Z

I think we need to add https://github.com/kubernetes-sigs/kueue/issues/4 to the list, I will work on that.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-03T02:46:32Z

also https://github.com/kubernetes-sigs/kueue/issues/91

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-04T21:00:11Z

check mark `Publish image https://github.com/kubernetes-sigs/kueue/issues/52`

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-11T14:26:10Z

Check `Single heap per Capacity https://github.com/kubernetes-sigs/kueue/issues/87` ✅

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-11T21:27:17Z

we have an image!!!
`gcr.io/k8s-staging-kueue/kueue:devel`

```bash
[eduardo@fedora-workstation kueue]$ skopeo list-tags docker://gcr.io/k8s-staging-kueue/kueue
{
    "Repository": "gcr.io/k8s-staging-kueue/kueue",
    "Tags": [
        "devel"
    ]
}
```

Prow job: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/post-kueue-push-images/1502394011774619648

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-14T13:58:04Z

CHeckMark -> `Queue status https://github.com/kubernetes-sigs/kueue/issues/5`

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-01T18:07:37Z

Checkmark Event for unschedulable workloads https://github.com/kubernetes-sigs/kueue/issues/91

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-08T15:33:14Z

checkmark `User guide https://github.com/kubernetes-sigs/kueue/issues/64`

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-08T19:32:14Z

@ahg-g @denkensk @ArangoGutierrez PTAL at the draft for release notes in the issue description.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-08T20:14:22Z

can we use https://github.com/kubernetes-sigs/kueue/blob/main/.github/ISSUE_TEMPLATE/NEW_RELEASE.md ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-08T20:19:20Z

Opened #197

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-09T19:38:10Z

A couple of other renames we should do: 
1. cq.requestableResources -> resources
2. cq.flavor.resourceFlavor -> cq.flavor.name

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-10T15:52:49Z

Before the first release we need to ignore jobs with queue name not set; this is important so users are not surprised that their existing running jobs get suspended when they first try Kueue.

We will add a flag to ComponentConfig to disable this behavior, and a namespace selector to select which namespaces the job-controller will take over. We can do that in the next release.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-11T13:48:11Z

sgtm, can you open an issue and/or PR?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-11T13:51:52Z

I will address the two comments above once the multiple api groups pr merges

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-11T14:23:35Z

> A couple of other renames we should do:
> 
> 1. cq.requestableResources -> resources
> 2. cq.flavor.resourceFlavor -> cq.flavor.name

+1 to both

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-11T18:28:14Z

https://github.com/kubernetes-sigs/kueue/pull/205 disables reconciling jobs with no queue name set.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-11T18:49:38Z

and https://github.com/kubernetes-sigs/kueue/pull/206 for renaming requestableResources in the api.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-12T01:11:04Z

and https://github.com/kubernetes-sigs/kueue/pull/207 for component config

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-12T17:17:37Z

All items are complete. We probably leave the nice-to-have issues for the next release.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-12T17:17:47Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/63#issuecomment-1096989542):

>All items are complete. We probably leave the nice-to-have issues for the next release.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
