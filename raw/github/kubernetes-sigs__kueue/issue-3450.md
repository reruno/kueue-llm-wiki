# Issue #3450: TAS: Graduate to Beta

**Summary**: TAS: Graduate to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3450

**Last updated**: 2025-09-30T12:49:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-05T10:05:38Z
- **Updated**: 2025-09-30T12:49:35Z
- **Closed**: 2025-09-18T08:45:46Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 19

## Description

**What would you like to be added**:

Provide implementation for the features required for Beta: https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling#beta

Probably the most important task is to put pods with consecutive indexes (ranks) within the same topology domain.

This may take a while, and potentially we release a second alpha, so I don't say yet "promote to beta".

This is continuation of https://github.com/kubernetes-sigs/kueue/issues/2724

The rank-based ordering issue: https://github.com/kubernetes-sigs/kueue/issues/3533

**Why is this needed**:

To prepare for promotion to Beta

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T10:06:29Z

cc @tenzen-y @mwielgus

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-18T17:51:10Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T17:51:52Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-19T18:09:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-18T18:10:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-19T09:28:49Z

/remove-lifecycle rotten

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-08-25T19:31:21Z

@mimowo Hello, is there any specific item on this issue that could use some help?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T09:38:07Z

> [@mimowo](https://github.com/mimowo) Hello, is there any specific item on this issue that could use some help?

We are currently evaluating some of TAS scheduling profiles based on user feedback. So, we would like to wait for the graduation for a while.
cc @mwysokin @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-03T15:05:17Z

> @mimowo Hello, is there any specific item on this issue that could use some help?

We are revisiting this topic for 0.14. Let me think how we could divide the work.

> We are currently evaluating some of TAS scheduling profiles based on user feedback. So, we would like to wait for the graduation for a while.

I think the TAS scheduling profiles are behind other dedicated TAS feature gates. New capabilities can always be added as extensions to Beta or GA features. Indeed, we are considering tuning the placement algorithms / profiles, or configuring them based on user feedback, but this could take long.

I think graduation of the main feature gate (TopologyAwareScheduling) and the API should not be blocked by that.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T17:58:39Z

/retitle TAS: Graduate to Beta

To make it more goal-oriented

/assign
I'm going to look into details of what is the MVP for graduating to Beta, possibly in 0.14

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T17:13:14Z

We would like to graduate TAS to beta. Here is a [tentative plan doc](https://docs.google.com/document/d/1UK_DnZ1Q4sUz8u9hYUTJexfw79z8pYwd9dtXEvXoEuE/)

I'm going to bring it up on the next wg-batch sync. PTAL.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-15T09:26:33Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:30:45Z

I have discussed the Graduation plan for TAS to Beta and collected some early feedback from users already.

An important feedback we get is that TAS without Node Hot Swap is far from ideal. The issue is that without TAS when a Pod fails, then kube-scheduler is free to schedule the replacement Pod immediately on the entire cluster. This is not the case for "core" TAS without Node Hot Swap, because the set of nodes to use it written into the Workload's Status object in the [TopologyAssignment](https://github.com/kubernetes-sigs/kueue/blob/1ffa6bd6cbe6df67c0b51cfc7514af11697fd469/apis/kueue/v1beta1/workload_types.go#L238) status.
As a consequence, when a node listed in the assignment fails, then topologyUngater will not be able to "ungate" the Pod, and kube-scheduler will not be able to act on the Pod. **The early feedback indicates** this is prohibitive to use TAS for some users, and would be considered regression if they migrated to TAS.

So, we reviewed the state of the Node Hot Swap with @PBundyra and @pajakd and summarized the current state in the updated documentation https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#feature-gate-interaction-matrix. Based on the feedback we believe the most anticipated configuration is to enable all three gates by default: TASFailedNodeReplacement, TASReplaceNodeOnPodTermination, TASFailedNodeReplacementFailFast.

Now, we acknowledge the triggering of the Node Hot Swap is "heuristics based", and so we may need to have some configuration knobs to satisfy various user requirements. However, this combination seems to be what the users who provided the early feedback are looking for. 

So, as a path forward I propose:
- along with graduating TAS to Beta we graduate Node Hot Swap "TASFailedNodeReplacement, TASReplaceNodeOnPodTermination, TASFailedNodeReplacementFailFast" to Beta
- we add a graduation criteria for TAS to GA to provide a knob for all requested modes of operation for Node Hot Swap (looking forward to the community feedback)
- for now users who don't want to enable Node Hot Swap will be free to disable the feature gates

cc @tenzen-y @gabesaba  @kannon92 @mwysokin @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:49:47Z

@mbobrovskyi assuming we go with this recommendation could you please prepare a follow up PR on top of https://github.com/kubernetes-sigs/kueue/pull/6830 to graduate Node Hot Swap feature gates?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-17T13:35:16Z

@mimowo Thank you for summarizing that. I totally agree with the result.

> we add a graduation criteria for TAS to GA to provide a knob for all requested modes of operation for Node Hot Swap (looking forward to the community feedback)

This is important for me because the cluster/node sometimes reports an unintended no healthy status, and there are different Node Availability criteria based on the cluster environment, and the current Node hot swap does not provide a fine-grained specifying way. So, I would propose to provide a way to disable the node hot swap feature (or provide hot swap strategies like None, PodTermination, and more) before GA graduation, then generalize such criteria or just document the way to tune the available criteria after GA graduation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:26:00Z

Make sense, I retitled the issue to reflect the need for configuration: https://github.com/kubernetes-sigs/kueue/issues/6514#issuecomment-3303267316

still, I think enabling all the gates seems like a sensible default behavior

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T09:11:55Z

Since we graduate the Topology API from Alpha to Beta I think we need some "update procedure". It might be manual as we did for MultiKueue in 0.9 or Cohorts in 0.13. 

@mbobrovskyi would you like to prepare a markdown snippet we could use to update the notes  https://github.com/kubernetes-sigs/kueue/issues/6756?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-09-18T11:17:58Z

SGTM 🖖

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-30T12:49:35Z

## Upgrading steps

### 1. Back Up Topology Resources (skip if not using Topology API):

```sh
kubectl get topologies.kueue.x-k8s.io -o yaml > topologies.yaml
```

### 2. Update apiVersion in Backup File (skip if not using Topology API):
Replace `v1alpha1` with `v1beta1` in topologies.yaml for all resources:

```sh
sed -i -e 's/v1alpha1/v1beta1/g' topologies.yaml
```

### 3. Delete Old CRDs:

```sh
kubectl delete crd topologies.kueue.x-k8s.io
```

### 4. Remove Finalizers from Topologies (skip if not using Topology API):

```sh
kubectl get topology.kueue.x-k8s.io -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' | while read -r name; do
  kubectl patch topology.kueue.x-k8s.io "$name" -p '{"metadata":{"finalizers":[]}}' --type='merge'
done
```

### 5. Install Kueue v0.14.x:
Follow the instructions [here](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) to install.

### 6. Restore Topology Resources (skip if not using Topology API):

```sh
kubectl apply -f topologies.yaml
```
