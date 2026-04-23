# Issue #9019: Support topology-domain–scoped admission eligibility in TAS

**Summary**: Support topology-domain–scoped admission eligibility in TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9019

**Last updated**: 2026-02-09T16:05:58Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-02-06T07:57:24Z
- **Updated**: 2026-02-09T16:05:58Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

Kueue needs a way to exclude entire TAS topology domains from admission-time placement based on domain lifecycle state, in order to support correct scheduling and lifecycle management for topology-sized workloads.

**What would you like to be added**:

Kueue Topology Aware Scheduling (TAS) derives topology domains implicitly by grouping nodes via configured topology levels and performs admission-time placement decisions based on node-level state. However, while Kueue TAS derives topology domains for placement, it does not currently have a mechanism to associate lifecycle or eligibility state with those domains or to enforce domain-scoped admission constraints.

This limitation prevents Kueue from enforcing admission constraints that apply to an entire topology domain (for example, an NVLink-sized domain) and leads to known failure modes where late-admitted long-running workloads can indefinitely block maintenance or other lifecycle operations.

This issue proposes adding **admission-time eligibility filtering at the topology-domain level**, based on externally provided domain state, as a an extension to existing TAS behavior.

**Why is this needed**:

In environments with large, topology-sized allocation units (for example, NVLink domains, racks, or fabric partitions), certain operations such as maintenance must be performed **at the topology-domain granularity**.

Today, Kueue can:

* reason about node-level state,
* derive topology domains from labels, and
* perform atomic placement across those domains.

However, it cannot express intent such as:

* “do not admit new long-running workloads into this topology domain”
* “this domain is preparing for maintenance”
* “this domain may accept opportunistic workloads only”

As a result, admission-time decisions cannot prevent late workloads from landing in a domain that is expected to drain, causing tail workloads that delay maintenance indefinitely.

Node-level mechanisms (for example, taints) are insufficient because they:

* operate at per-node granularity,
* are enforced after admission by kube-scheduler, and
* cannot guarantee atomic, domain-wide placement decisions.

**Completion requirements**:

Extend Kueue admission to support **topology-domain–scoped eligibility filtering** during TAS placement.

At admission time:

1. Kueue builds the topology snapshot as it does today.
2. For each derived topology domain, Kueue consumes an external signal representing domain lifecycle or eligibility state.
3. Domains whose state is incompatible with the incoming workload are excluded from placement consideration.
4. TAS placement runs only on the remaining eligible domains.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

### Relationship to Existing Discussions

This issue is related to prior discussions around group-level or topology-scoped admission constraints (for example, #5147), but focuses on a **concrete, TAS-based use case** where topology domains already exist and only lifecycle state is missing.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T08:17:11Z

Hm, we support in TAS taints & tolerations as well as `NodeAffinity.requiredDuringSchedulingIgnoredDuringExecution`. 

So, I believe some of the use cases, maybe not most conveniently, but could be supported with the current mechanisms. For example an admin could add dedicated Taints to a group of nodes (in a domain like node-pool, rack, block, etc.), and a user could create w workload to match this group of nodes with  `NodeAffinity`. 

Before we jump into "solving the problem" I would like to really understand what are the use cases which cannot be achieved with the current tooling.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-08T00:00:51Z

Thanks for calling this out, that’s a fair question.

I agree that with TAS today we *can* approximate some forms of domain steering using a combination of taints, tolerations, and `NodeAffinity.requiredDuringSchedulingIgnoredDuringExecution`. For certain static or coarse-grained use cases, especially when the domain is relatively stable and the intent is long-lived, those tools can be made to work, albeit somewhat indirectly.

The gap I’m trying to highlight is narrower and more specific, and it shows up around **admission-time guarantees and atomicity at the topology-domain level**.

Concretely, the use case we’re struggling to model is not “how do I steer workloads into a particular domain,” but rather:

* how to **prevent admission of new long-running workloads into a topology domain that is preparing for maintenance**, and
* how to do so **atomically at the domain level**, rather than incrementally at the node level.

Even if an admin taints all nodes in a rack or sub-block, the system still reasons about schedulability on a per-node basis. During transitions, there is almost always a window where at least one node remains eligible, and TAS can still form a placement. That’s enough to admit “just one more” long-running workload, which then pins the entire domain and defeats the maintenance intent.

From our perspective, this is the key distinction:

* **Taints / affinity answer:** “May this pod run on this node?”
* **The missing primitive answers:** “Is this topology domain eligible for admitting this *class of workload* right now?”

That decision needs to happen **before admission and before placement**, and it needs to apply to the domain as a whole, not be derived implicitly from per-node state.

So I don’t think the current mechanisms are wrong or insufficient in general, but they don’t give us a clean way to express *domain-level lifecycle intent* (e.g., “maintenance-pending, allow only opportunistic workloads”) in a way that admission can reason about deterministically.

I’m very open to being proven wrong here, and I’d actually love to sanity-check this together. If there’s a way to encode this particular maintenance-alignment scenario using today’s TAS + taints/affinity **without** risking partial admission into a draining domain, that would be great to explore. My suspicion is that once we require admission-time, domain-atomic guarantees, we’re outside what node-scoped primitives can safely provide, which is what led us to raise this as a potential gap rather than jumping straight to a solution.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T11:31:45Z

Oh, now I see what you mean. Indeed there is a gap in Kueue, but if we relax the expectations then this could be achieved in the following flow:
1. admin adds the NoSchedule taint to all nodes matching a certain label (domain). this can be done for example `kubectl taint nodes -l topology-rack=myrack key=value:NoSchedule` to prepare the domain for maintenance
2. after a while the admin can issue: `kubectl taint nodes -l topology-rack=myrack key=value:NoExecute`  to make sure the nodes are getting evicted

We are currently working on the support here: https://github.com/kubernetes-sigs/kueue/issues/8828

Once we have the support for handling taints in TAS, then I think the only gap if IIUC is atomicity, but I think this will work well in practice, because the command ``kubectl taint nodes -l topology-rack=myrack key=value:NoSchedule`  will issue requests with very small intervals, probably within 10ms, unless you have really huge domains (>100 nodes probably).

Even if some workload gets partially scheduled (very unlikely), then with the new work on taint support it will get evicted and re-admitted. 

So, while I agree we could try to achieve Taints per domain (rather than Node) it looks like a lot of effort / gain, we are going to have the per-node support for tainting. Let me know if I'm missing something.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-09T16:05:58Z

> So, while I agree we could try to achieve Taints per domain (rather than Node) it looks like a lot of effort / gain, we are going to have the per-node support for tainting. Let me know if I'm missing something.

You’re not missing anything, I agree with your assessment. In practice, we can approximate this today using existing Kubernetes primitives at the node level, and that’s likely what we would do in the short term.

The limitation is not the taint or label mechanism itself, but the fact that taints and labels are applied incrementally across nodes within a domain. This behavior exists for all domains, but becomes increasingly pronounced as the domain size grows, which can leave the domain in a partially available state for some period of time and make the effective domain state ambiguous.

The core of the proposal is therefore not “domain taints vs node taints”, but introducing an explicit domain-level signal that Kueue can reason about directly. If a domain is represented as a first-class object, Kueue TAS can observe its spec and status to determine whether a workload is suitable for that domain (globally or for a given workload class), without descending to per-node inspection.

The key benefit is atomicity and clarity: a domain is either eligible or not eligible, rather than transiently and partially eligible depending on the progress of node-level updates. Achieving that level of precision is difficult with node taints and labels alone, especially at larger scales.
