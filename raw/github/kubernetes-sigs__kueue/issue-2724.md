# Issue #2724: Topology Aware Scheduling (Alpha)

**Summary**: Topology Aware Scheduling (Alpha)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2724

**Last updated**: 2024-11-05T15:19:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-30T10:40:54Z
- **Updated**: 2024-11-05T15:19:48Z
- **Closed**: 2024-11-05T15:19:45Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 14

## Description

**What would you like to be added**:

Ability to control how closely the pods are packed on nodes in a data center. 

Currently, a user of Kueue, like AI/ML researcher, has no way of telling "run this workload so that all pods are on nodes within a rack (or block)".  Running a workload with Pods scattered across a data center results in longer runtimes, and thus costs. 

**Why is this needed**:

To reduce the codes of running AI/ML workloads which require exchanging huge amounts of data over network.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T10:41:01Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T10:41:14Z

/cc @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-30T14:46:06Z

@mimowo What is the reason that you do not prefer ResourceFlavor taints instead of dedicated fields?
If I am missing any context, please let me know.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T14:55:20Z

> @mimowo What is the reason that you do not prefer ResourceFlavor taints instead of dedicated fields?
> If I am missing any context, please let me know.

Sure, I will be happy to explain, but I'm not sure I understand: which fields do you mean? 

Maybe this is related to your question (I'm not sure 100%), but a RF can have a set of labels which have nothing to do with topology. For example, they can be to choose a GPU family.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-30T15:03:41Z

> > @mimowo What is the reason that you do not prefer ResourceFlavor taints instead of dedicated fields?
> > If I am missing any context, please let me know.
> 
> Sure, I will be happy to explain, but I'm not sure I understand: which fields do you mean?
> 
> Maybe this is related to your question (I'm not sure 100%), but a RF can have a set of labels which have nothing to do with topology. For example, they can be to choose a GPU family.

Let me check the "GPU family" mean. Which K8s features can be represented the GPU family? Node Label? or Node Taints? or other features?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-31T08:27:06Z

> Let me check the "GPU family" mean. Which K8s features can be represented the GPU family? Node Label? or Node Taints? or other features?

This was just an example, what I meant is that nodes have labels. Some labels correspond to topology (the new ones, for example `cloud-provider.com/topology-block`, or `cloud-provider.com/topology-rack`), and some don't (like `cloud.google.com/machine-family`). 

Maybe it can be clearer when looking at the example table in: https://github.com/kubernetes-sigs/kueue/blob/5d7847bed87ffa353732164de229b0f94aeab8bd/keps/2724-topology-aware-schedling/README.md#hierarchy-representation.

I think two things are important for design choice:
- it is not feasible for an admin to create RFs per rack to match it using the existing API if you have thousands or racks in a cluster
- some workloads may not fit within a single rack. Still, we want Kueue to compactify the placement of pods so that the number of used racks is minimal. So, some pods with have the value of the label `cloud-provider.com/topology-rack: rack1` while others `cloud-provider.com/topology-rack: rack2`. This is not expressible with the current API.

I think we can discuss specific details of the API or alternatives in the KEP.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-09-03T21:46:31Z

@tenzen-y, how quickly will this slam the queuing algorithm if each `rack` needs to be treated as a different flavor? I know there's limits on the number of flavors that can be defined by a `ClusterQueue` currently at around 8 or so. @mimowo mentioned thousands of racks. I get the feeling that this should be handled at the scheduler level not at the queuing level.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T15:19:01Z

> @tenzen-y, how quickly will this slam the queuing algorithm if each `rack` needs to be treated as a different flavor? I know there's limits on the number of flavors that can be defined by a `ClusterQueue` currently at around 8 or so. @mimowo mentioned thousands of racks. I get the feeling that this should be handled at the scheduler level not at the queuing level.

@KPostOffice Thank you for catching up and giving me your feedback. I added a similar concern here: https://github.com/kubernetes-sigs/kueue/pull/2725#discussion_r1754907510

Let's discuss that in the KEP PR.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-22T10:13:40Z

FYI @tenzen-y @gabesaba @PBundyra @mwielgus 
I have opened a spreadsheet to keep track of the remaining work (planned in KEP and follow ups): [spreadsheet](https://docs.google.com/spreadsheets/d/1MXCjKZtAfqBTb61bJo46u7jIUqRIlu1NrYj1L8Xz-UU/edit?resourcekey=0-gr1ML2A1Axi8s6Lxr-Zhlw&gid=0#gid=0)

It is shared with wg-batch@kubernetes.io, a couple of folks who are involved in reviews, and on-demand.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T15:57:04Z

@tenzen-y when the alpha phase is ready do you think we should split the issue into "Topology Aware Scheduling (Alpha)" and "Topology Aware Scheduling (Beta)" and close the one for Alpha, or we reuse the issue for Beta graduation?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T18:21:10Z

> @tenzen-y when the alpha phase is ready do you think we should split the issue into "Topology Aware Scheduling (Alpha)" and "Topology Aware Scheduling (Beta)" and close the one for Alpha, or we reuse the issue for Beta graduation?

I'm ok with either way.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T10:11:31Z

I decided to split so that Alpha is visible as closed on the list here: https://github.com/kubernetes-sigs/kueue/issues/3192 (I will close it soon before the release as we still have some small improvements pending like https://github.com/kubernetes-sigs/kueue/pull/3445)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T15:19:41Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T15:19:45Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2724#issuecomment-2457453326):

>/close 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
