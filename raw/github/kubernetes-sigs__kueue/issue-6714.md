# Issue #6714: MultiKueue: support authentication to worker clusters using ClusterProfile

**Summary**: MultiKueue: support authentication to worker clusters using ClusterProfile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6714

**Last updated**: 2025-11-19T15:20:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-03T12:53:22Z
- **Updated**: 2025-11-19T15:20:02Z
- **Closed**: 2025-11-19T15:20:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@hdp617](https://github.com/hdp617)
- **Comments**: 9

## Description

**What would you like to be added**:

An integration with [ClusterProfiles](https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/5339-clusterprofile-plugin-credentials).

**Why is this needed**:

- Currently we use for authentication long-living secrets generated for worker clusters. Some users are cautious about long-living secrets. They could be rotated / regenerated, but it is an extra effort.
- ClusterProfile is an important k8s API designed for managing multiple clusters. It seems still Alpha, but we could start the integration early.
- - Easier setup for providers supporting Workload Identity mechanism

**Completion requirements**:

We could start with a prototype.

This enhancement requires the following artifacts:

- [ ] Design doc (probably an extension to the MultiKueue KEP)
- [ ] API change (probably to determine which authentication is to be used)
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-03T12:55:42Z

cc @tenzen-y @gabesaba @mwysokin @mwielgus @mbobrovskyi

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-03T15:03:24Z

cc @haoqing0110 

I know your group has been involved in sig-multicluster so I'd love your thoughts also.

### Comment by [@linde](https://github.com/linde) — 2025-09-03T20:45:46Z

cc @corentone, @hdp617, @knee-berts, @zhang-xuebin

### Comment by [@linde](https://github.com/linde) — 2025-09-03T20:51:37Z

/assign @hdp617

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-03T20:51:40Z

@linde: GitHub didn't allow me to assign the following users: hdp617.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6714#issuecomment-3250754140):

>/assign @hdp617


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@hdp617](https://github.com/hdp617) — 2025-09-03T21:16:55Z

Thanks for creating this issue! We've had some discussions about using the ClusterProfile API and the credential plugins introduced in [KEP-5339](https://github.com/kubernetes/enhancements/blob/master/keps/sig-multicluster/5339-clusterprofile-plugin-credentials/README.md) for cluster authentication. Happy to take this one.

### Comment by [@haoqing0110](https://github.com/haoqing0110) — 2025-09-04T03:56:18Z

OCM (Open Cluster Management) community is planning to [support ClusterProfile credentials plugin](https://github.com/open-cluster-management-io/ocm/issues/1163). And we're very happy to see that MultiKueue supports ClusterProfile, this will bring benefits to the current [ OCM + MultiKueue integration](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/#optional-setup-multikueue-with-open-cluster-management).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T06:56:27Z

/assign @hdp617
Thanks for willing to work on it 👍

### Comment by [@kishorerj](https://github.com/kishorerj) — 2025-09-06T10:09:21Z

I am open to contribute on this as well.. We have few customers in GKE who need this feature @hdp617  @mimowo
