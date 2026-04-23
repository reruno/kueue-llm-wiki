# Issue #6334: Add native Kueue support for ReplicaSets and Deployments

**Summary**: Add native Kueue support for ReplicaSets and Deployments

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6334

**Last updated**: 2026-04-13T16:22:36Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-07-31T16:23:50Z
- **Updated**: 2026-04-13T16:22:36Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `priority/important-longterm`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 29

## Description

**Description:**

Kueue currently supports Kubernetes `Deployment` workloads only via **pod-integration mode**, where pods created by the ReplicaSet are directly matched to Workloads. This mode is functional but lacks the benefits of Kueue-native integration, such as proper quota management, slice-based scheduling, and improved admission control.

With the addition of the `WorkloadSlices` feature in the **v0.13.0 release**, it is now feasible to implement native Kueue support for `ReplicaSet`, which is the underlying controller for `Deployment` objects. Doing so would enable:

* Proper handling of scaling and slicing logic via WorkloadSlices
* Kueue-native admission and reclamation behavior
* Better integration with quota-based capacity tracking
* Simplified support for higher-level abstractions like `Deployment`, `StatefulSet`, etc.

**Proposal:**

* Add a new adapter for `ReplicaSet` that supports:

  * Workload creation and updates using WorkloadSlices
  * Admission lifecycle handling
  * Reclaim signaling and suspension
* Extend the Deployment compatibility documentation to clarify that native support is now available when used in conjunction with WorkloadSlices.

**Motivation:**

Native support for `ReplicaSet` would eliminate the need for pod-level tracking for common use cases and simplify the adoption of Kueue for standard Kubernetes workloads like `Deployment`, especially in multi-tenant environments.

**Additional context:**

This enhancement builds on top of the `WorkloadSlices` KEP (KEP-77), and would serve as a model for adapting other built-in controllers.

### Problem Statement

Today, Deployments can be integrated with Kueue via Pod Integration (PI), where each Pod is represented as an individual Workload. While functional, this model exposes several limitations that become more pronounced at scale and in advanced use cases.

#### 1. Limitations of Deployment + Pod Integration

Under Pod Integration, a Deployment is effectively decomposed into a set of independent Workloads (one per Pod). This creates several challenges:

* **Loss of coordination semantics**
  There is no notion of a Deployment-level unit. Pods are admitted independently, which prevents expressing coordinated behaviors such as:

  * gang-style scale-up (all-or-nothing admission)
  * coordinated eviction or rollback

* **Fragmentation and operational overhead**
  A single Deployment results in many Workloads, increasing control-plane load and making observability, debugging, and reasoning about state more difficult.

* **No flavor consistency guarantees**
  Since Pods are admitted independently, even Pods with identical shape (e.g., belonging to the same ReplicaSet) may be placed on different ResourceFlavors. This leads to heterogeneous placement within what is logically a single version of the application, resulting in inconsistent performance characteristics and topology misalignment.

* **Lack of MultiKueue support**
  In a MultiKueue setup, Pod-level Workloads are propagated independently across clusters, with no coordination between them. This effectively means:

  * no Deployment-level synchronization across clusters
  * no consistent rollout or admission semantics
  * no clear unit of placement or failover

  As a result, Deployment + PI does not provide meaningful MultiKueue support.

#### 2. Why Kueue-native Deployment support

Introducing native Deployment support in Kueue aims to address these limitations by elevating the abstraction level from Pod to Deployment (or a closely aligned unit such as ReplicaSet).

Key goals include:

* **Unified capacity management**
  Treat Deployment as a coherent unit for quota accounting and admission, rather than a collection of independent Pods.

* **Coordinated admission and scaling semantics**
  Enable expressing higher-level behaviors such as:

  * all-or-nothing scale steps
  * controlled rollout under capacity constraints

* **Better alignment with Kubernetes lifecycle**
  Leverage existing Kubernetes abstractions (e.g., ReplicaSets) to model updates and scaling in a way that preserves native semantics.

* **Flavor-aware placement semantics**
  Provide consistent placement for Pods belonging to the same ReplicaSet (i.e., identical-shape Pods share the same ResourceFlavor), while allowing flexibility across ReplicaSets during updates (e.g., new versions may land on different flavors if required by scheduling or constraints).

* **Foundation for MultiKueue support**
  Provide a meaningful unit of propagation and coordination across clusters, enabling consistent placement and rollout behavior.

#### 3. Design space

Given the above, the design space for Kueue-native Deployment support includes:

* modeling at the ReplicaSet level (aligned with Kubernetes update/scale boundaries)
* modeling at the Deployment level (requiring additional semantics for mutability and rollout coordination)

The choice between these approaches depends on which constraints and semantics we prioritize, particularly around mutability, rollout handling, and scheduler behavior.


/kind feature

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T18:28:40Z

Maybe I'm missing something but I'm sceptical about supporing ReplicaSets as first class citizens (workloads) in Kueue. No user requested so far having Workload or Quota management at the ReplicaSet level.

If we want to support Deployments in Kueue via WorkloadSlices we may need to interact with ReplicaSets but I think this should remain a technical detail.

Also, the support for Deployments is questionable as they are used for serving where Pods don't talk to each other and so we can handle them independently, workload per pod.

AI inference workloads often require collective work, but for this use case LWS is a better user choice, and Kueue already allows for scalability group by group.

I'm open to hear there are use cases for managing Deployments as full workloads, but I prefer to clarify this use case first.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-31T22:01:06Z

Thank you for the thoughtful response, @mimowo!

> No user requested so far having Workload or Quota management at the ReplicaSet level.

Hooray, then this issue can be the first request! 🎉
We’re definitely interested in seeing Kueue support both `Deployment` and `ReplicaSet` as first-class workloads. Our goal is to enable native integration that benefits from proper quota management, admission control, and scheduling behavior, beyond what pod-level integration currently provides.

You're right that no users have explicitly requested quota or workload-level control on `ReplicaSet` or `Deployment` objects, but I’d argue this might be more a matter of discoverability than lack of demand. Most users operate in terms of `Deployment` (or other higher-level abstractions), and since today these are only supported via pod-integration, the benefits of Kueue-native behavior, such as proper quota tracking, admission, and preemption, are not visible or accessible in that path.

> If we want to support Deployments in Kueue via WorkloadSlices we may need to interact with ReplicaSets but I think this should remain a technical detail.

True, though it's worth noting that `ReplicaSet` is itself a top-level Kubernetes resource with its own lifecycle. While it's uncommon, users can and do manage `ReplicaSet` resources directly, outside of the `Deployment` abstraction, similar to how `Job` can exist outside the `CronJob` context. If Kueue’s goal is to support Kubernetes-native types uniformly, treating `ReplicaSet` as a first-class workload could be consistent with that direction.

> Also, the support for Deployments is questionable as they are used for serving where Pods don't talk to each other and so we can handle them independently, workload per pod.

I suspect the same argument could be made for any current Kueue integration. The core concern with Deployment support via pod-integration is the inability to treat the workload holistically in terms of key Kueue constructs, quota enforcement, workload-level admission, and preemption. While it’s technically feasible to use pod-integration for any framework, it’s ultimately suboptimal for these reasons, the same reasons Kueue added native adapters for other controllers.

> AI inference workloads often require collective work, but for this use case LWS is a better user choice, and Kueue already allows for scalability group by group.

I can't speak directly to inference or LWS, they're outside our current scope. From our perspective, Kueue offers powerful primitives for workload and quota management that are applicable across a wide variety of workload types. Our goal is to improve and broaden the user experience for those using standard Kubernetes constructs, including `Deployment`, without requiring them to adopt a specific workload framework.

> I'm open to hear there are use cases for managing Deployments as full workloads, but I prefer to clarify this use case first.

Happy to expand on our specific use cases (probably best done offline). At a high level, we want to be able to run `Deployment` and `StatefulSet` workloads outside of pod-integration so we can take full advantage of Kueue’s workload-level behavior, including quota management, admission, and preemption, in a way consistent with how other supported frameworks are treated.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T06:57:22Z

I think there are some undisputed parts to the issue and some which require more discussion or even dropping. Let me try to untangle a little bit.

First, I wouldn't call the support via WorkloadSlices, but ElasticJobs. I want to maintain the WorkloadSlizes as a technical detail which can be replaced (potentailly, TBD by WorkloadResize), so I prefer to minimize the API surfing ./ naming to  minimum.

On that note we probably should have called the feature ElasticWorkloads, but it is not too bad as is.

Now, let me split comments by type:
- StatefulSets (not mentioned in title): no dispute here.

- Deployments, fair. I just wanted to point out that from discussions so far users are typically wan Deployments to self-adjust to available quota and run say at 50% capacity (to meet users requirement to ensure say Deployemnt is always >20% available we discussed in the past combining Workloads per pod into fragments and never preempting more than 90% fragments). Also, it is typically desired for users to allow to scatter the  pods across ResourceFlavors, because they are  independent so no need to optimize for bin packing. 

Having said that I'm onboard to support them, especially as it will make easier to achieve the feature of co-locating all Deployment pods in a single cluster in MultiKueue which was requested by some users. Given pros and cons we will need to support both ways I think in the long run. 

- ReplicaSet - here and only here I have major hesitation. Yes, ReplicaSet is an API at the Kubernetes level, but it is not really UX-meant API. Even k8s  documentation says: "Usually, you define a Deployment and let that Deployment manage ReplicaSets automatically.", and "Therefore, we recommend using Deployments instead of directly using ReplicaSets, unless you require custom update orchestration or don't require updates at all.".  I don't know any UX use-case which requires ReplicaSet, instead of Deployments.

Since Kueue is a UX-layer framework I'm think we don't really need to support ReplicaSets as first class citizens. 

On top of that:
- we already support it as second-class citizens via Pod integration if users put the queue-name label into PodTemplate.
- there would be a significant prerequisite work required even when ElasticJobs is disabled (I think separate pre-requisite issue). 

When maintaining a project we need each time to weigh the benefit to cost (maintenance, complexity, documentation) ratio. Thus, while remaining open about this possibility I'm flagging concerns.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-01T08:20:11Z

Thanks for sharing your perspective, @mimowo.

> Since Kueue is a UX-layer framework I'm think we don't really need to support ReplicaSets as first class citizens.

I definitely understand the hesitation around treating ReplicaSets as first-class citizens, especially since Kubernetes documentation positions them as lower-level primitives primarily managed by Deployments.

That said, from my point of view, adding support for ReplicaSets in Kueue isn't about promoting them as a UX-facing API. Rather, it's an enablement mechanism for fully supporting Deployments. Since Deployments manage their lifecycles via ReplicaSets, any meaningful native integration (e.g., quota tracking, admission control, or preemption) will likely require us to interact with the underlying ReplicaSet objects — even if the user only interfaces with the Deployment.

By this token, the current pod-integration support for Deployments arguably introduces even greater inconsistency with Kueue's role as a UX-layer framework, since Kueue treats Pods as first-class citizens, even though Pods are abstracted by ReplicaSets, which in turn are abstracted by Deployments. Supporting ReplicaSets would help bridge that abstraction gap and improve alignment with the actual object hierarchy Kubernetes uses to realize Deployments.


> * we already support it \[Deployment] as second-class citizens via Pod integration if users put the queue-name label into PodTemplate.

This is a fair point. In my view, supporting Deployments as a Kueue-native framework is mutually exclusive with supporting them via pod-integration. We would need a mechanism that allows users to choose one approach over the other, ideally as a global configuration in Kueue (preferred), or optionally overridden per workload, or possibly a combination of both.

> When maintaining a project we need each time to weigh the benefit to cost (maintenance, complexity, documentation) ratio. Thus, while remaining open about this possibility I'm flagging concerns.

Absolutely, I fully agree that we need to carefully weigh the benefit-to-cost ratio, especially with respect to long-term maintenance, complexity, and documentation. I appreciate you flagging these concerns early.

That said, my intention here isn’t to increase surface area without clear justification, but rather to point out that native support for ReplicaSet (as an enabler) and Deployment could actually help reduce operational complexity. If proven to be a valuable alternative to pod-integration, this approach could eventually allow us to deprecate pod-integration for Deployments and StatefulSets, ultimately simplifying the codebase and improving maintainability in the long run.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T10:06:25Z

> That said, my intention here isn’t to increase surface area without clear justification, but rather to point out that native support for ReplicaSet (as an enabler) and Deployment could actually help reduce operational complexity. 

I hope with can support workload-level Deployments with ElasticJobs support without the need to support Workloads at the level of ReplicaSets. TBH, I'm not even totally sure why the ElasticJob would need to be aware of the ReplicaSet objects, I think it could just create the replacement workload to manage the quota. However, even if we need to be aware of the underlying ReplicaSet abstraction layer we can have a dedicated controller, without the need to have a workload for ReplicaSet. This is how we support LWS - StatefulSet even though it is a building block, it can be disabled as an integration.

>  If proven to be a valuable alternative to pod-integration, this approach could eventually allow us to deprecate pod-integration for Deployments and StatefulSets, ultimately simplifying the codebase and improving maintainability in the long run.

I don't see this happening, because users of Deployments value that the Pods can reserve quota in different flavors as they don't need to talk most often there is no need to bin pack them on the same node pool.

> By this token, the current pod-integration support for Deployments arguably introduces even greater inconsistency with Kueue's role as a UX-layer framework, since Kueue treats Pods as first-class citizens, even though Pods are abstracted by ReplicaSets, which in turn are abstracted by Deployments. Supporting ReplicaSets would help bridge that abstraction gap and improve alignment with the actual object hierarchy Kubernetes uses to realize Deployments.

I partly agree, but there is more context to it. 

First: Pods are a universal abstraction layer which can be used for basically all frameworks (open-source and in-house) - almost any framework can be supported at the level of PodGroups, which gives as a very nice tool. Kueue is designed as a project for batch workloads, and ReplicaSets are used for Deployments which are niche use cases (especially given raise of LWS for inference), so the Pod abstraction layer is way more universal for our users.
Second: For historical reasons we first supported Deployments only based on Pod integration enabled explicitly. Looking back at this we could enable PodIntegration for Deployments "implicitly" - without enabling them in ConfigMap. This is what we do supporting LWS. We have a reconciler for StatefulSet, even though we don't need to enable StatefulSet integration.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-01T17:55:21Z

> TBH, I'm not even totally sure why the ElasticJob would need to be aware of the ReplicaSet objects, I think it could just create the replacement workload to manage the quota.

I see where you're coming from, @mimowo, but I’d like to offer a different perspective.

Supporting Deployments as workload-level abstractions without acknowledging the ReplicaSet layer may be overly optimistic, especially in the context of ElasticJobs. ReplicaSets are not just implementation details; they're top-level Kubernetes objects with their own lifecycle, semantics, and controller reconciliation logic. Ignoring them or treating them as opaque intermediaries risks introducing edge cases or blind spots, particularly when dealing with scale-up and slice replacement behaviors.

When dealing with native Deployment support in Kueue, we need to be aware of two distinct lifecycle cases:

* **Scale** (up or down): Kubernetes delegates scaling to the *same* ReplicaSet object, which changes its `.spec.replicas` and `.status` accordingly.
* **Upgrade**: Kubernetes creates a *new* ReplicaSet in response to any Deployment update other than replica count (e.g., template change).

While it is technically possible to model and implement a Workload directly for a Deployment, I would argue that placing the Workload in closer proximity to the abstraction it actually represents, in this case, the ReplicaSet, yields multiple advantages:

* **1:1 mapping**: Each ReplicaSet is matched by a single Workload, providing a clean, well-scoped relationship that accurately tracks its lifecycle.

* **Upgrade handling**: When a Deployment is upgraded, Kubernetes gradually scales *down* the old ReplicaSet while scaling *up* the new one. This phased behavior is already well-aligned with how ElasticJobs manage multiple Workloads, treating them independently and scaling them according to the observed pod state.

  * As the old ReplicaSet scales down, the associated Workload reflects that.
  * As the new ReplicaSet scales up, a new Workload (or slice) is created in response.
  * Both cases are already well-supported by the current Kueue functionality.

* **Scale handling**: Since the actual increase or decrease in pod count happens at the ReplicaSet level, it makes ReplicaSet the ideal scope for workload placement. As the ReplicaSet scales down, so does the corresponding Workload. Similarly, when the ReplicaSet scales up, ElasticJob behavior kicks in, creating a new workload slice to represent the growing demand.

* Finally, as individual ReplicaSet instances go out of scope, e.g., via `revisionHistoryLimit`, so too would the corresponding Workloads naturally expire, keeping resource tracking clean and bounded.

In the grand scheme, I view this not as *adding* workload support to Deployments, but rather as *moving* or *lifting* existing support for Deployments from the “pod-level” abstraction (via pod-integration) to the more appropriate “ReplicaSet-level,” where lifecycle and intent are more explicitly modeled.

---

> However, even if we need to be aware of the underlying ReplicaSet abstraction layer, we can have a dedicated controller, without the need to have a workload for ReplicaSet.

I’m not convinced that introducing a dedicated controller *instead* of first-class ReplicaSet support would simplify things. On the contrary, it would likely increase the maintenance burden and architectural complexity. Such an approach would require custom logic to bridge the relationship between Deployments, ReplicaSets, and Workloads, something that first-class ReplicaSet support solves more directly and robustly.

A helpful analogy here is the relationship between `batchv1/CronJob` and `batchv1/Job` in Kubernetes. If we were to add native Kueue support for `CronJobs`, I’d argue the only integration needed would be minimal: primarily label and annotation assignment during admission, ensuring that the resulting `batchv1/Job` integrates cleanly with Kueue. There would be no need to hide the underlying `batchv1/Job` behind a complex controller abstraction.

Similarly, in this case, I view `Deployment` as a natural abstraction *extension* of `ReplicaSet`. The core workload lifecycle management, scaling, and upgrading happen at the `ReplicaSet` level. Therefore, it makes sense to model Workloads at that level and to treat `Deployment` as a thin wrapper requiring minimal, Deployment-specific logic.

By this analogy, I place native `ReplicaSet` and `StatefulSet` support in Kueue at the same tier: they are concrete, pod-managing controllers with well-defined lifecycle semantics. `Deployment`, like `CronJob`, builds on top of those and benefits from their support without needing to obscure or duplicate it.

---

> I don't see this happening, because users of Deployments value that the Pods can reserve quota in different flavors as they don't need to talk most often there is no need to bin pack them on the same node pool.

The flavor concept in Kueue—particularly how it relates to quota and Workload (PodSet) assignment, definitely warrants a separate and more focused discussion 🙂. I’ll follow up on that in a dedicated comment to avoid conflating the concerns here.

---

> Kueue is designed as a project for batch workloads, and ReplicaSets are used for Deployments which are niche use cases (especially given raise of LWS for inference), so the Pod abstraction layer is way more universal for our users.

I’d respectfully disagree with the characterization of Deployments (via ReplicaSets or otherwise) as a *niche* use case.

While Kueue is indeed designed with batch workloads in mind, the reality is that many real-world ML, data, and platform workflows still rely on Deployments as a foundational abstraction. These include inference services, streaming agents, data shippers, and other long-running, quota-sensitive workloads that don’t neatly fall under traditional batch APIs but still benefit significantly from workload-level scheduling and quota enforcement.

The very fact that we’re already support Deployments indirectly through pod-integration (explicitly or implicitly enabled via configs), reflects a clear demand from users who expect Kueue to interoperate with more than just batch Jobs. The issue with pod-level integration is precisely that it abstracts away too much, it fails to provide consistent quota tracking, lacks coordination during rollout or scaling events, and introduces subtle inconsistencies in preemption behavior. Native support at the ReplicaSet level addresses these limitations head-on.

Additionally, with the rise of elastic and burstable patterns (including LWS), we’re seeing increased interest in unifying quota and scheduling logic across workload types, batch or not. In that context, treating ReplicaSet as a proper workload type is not just reasonable, but a step toward broadening Kueue’s applicability in real clusters, especially in environments where users expect stronger consistency, preemption control, and scaling fidelity for non-batch use cases.

So while the *initial* Kueue scope may have been batch-focused, the growing adoption of mixed workload patterns suggests this isn’t a niche case, it’s a natural and timely evolution 🎉

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T18:28:26Z

Im not convinced, these remain my concerns:

Deployment upgrades require the same amount of quota during the process, we just replace all pods with new. We already support upgrades for StatefulSets, even have e2e tests and this works perfectly fine. Splitting this process into two workloads per ReplicaSet may delay the process due to the new for constant need of involving scheduler. This does not seem to be a scalable approach.

For scale we just need to scale quota, I see no need for managing ReplicaSets

I still think it is better to add custom controller than to extend API surface. Again this is what we decided to do fo LWS and it seems work well.

Im not saying that using Deployments is niche. Mixing inference and training, or serving and batch is use case we hear all the time. Maybe I didnt phrase my position properly. I think using ReplicaSets directly is the niche use case.

Tthe feature remains Alpha, and so Im not convinced it is good idea to already start pivoting designs in Kueue by that.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-01T20:13:32Z

> Deployment upgrades require the same amount of quota during the process, we just replace all pods with new. We already support upgrades for StatefulSets, even have e2e tests and this works perfectly fine. 

Respectfully, I have to fully disagree with the statement that *"Deployment upgrades require the same amount of quota."*

In practice, a Deployment update can introduce changes that directly affect quota requirements, beyond just the replica count. For example, the updated Pod template may:

* Add or remove containers (including init or sidecars),
* Modify the resource requests or limits for one or more containers.

These changes can significantly alter the quota footprint of the resulting ReplicaSet. So it's not simply a matter of "replacing all pods with new", the resource profile itself may differ between the old and new ReplicaSet.

Additionally, Deployment updates can include changes to fields like `nodeSelector`, which may (and arguably *should*) result in a different **flavor assignment** under Kueue. This is directly tied to quota accounting, as flavors partition capacity and quota tracking. Changing the flavor mid-rollout introduces further complexity that cannot be abstracted away as a “no-op” in terms of quota.

_Note_: this same class of changes is also possible in the context of StatefulSet updates. While I haven’t reviewed the current Kueue implementation for StatefulSet upgrades in detail, I’d expect that it correctly accounts for changes in resource profiles during rollout. If not, it’s certainly worth revisiting to ensure we’re not making similar incorrect assumptions there.

---

> Splitting this process into two workloads per ReplicaSet may delay the process due to the new for constant need of involving scheduler. This does not seem to be a scalable approach.

Perhaps there’s a misunderstanding here. There is no “splitting” involved in any form.

During a Deployment upgrade, what we observe is the natural outcome of Kubernetes’ rollout behavior: an existing (now outdated) ReplicaSet continues to scale down, while a new ReplicaSet is created and begins scaling up. In Kueue, each of these ReplicaSets is tracked independently by its corresponding Workload, using the existing **ElasticJob primitives**.

This model does *not* introduce artificial duplication or overhead. Instead, it mirrors what Kubernetes is already doing and gives us the opportunity to maintain accurate quota tracking and workload admission during transitional states.

In fact, one of the strengths of this approach is that it reuses existing Kueue functionality:

* As the **old ReplicaSet scales down**, its associated Workload gradually releases resources.
* As the **new ReplicaSet scales up**, a new Workload slice is created to reflect and manage that demand.

Crucially, this does not require introducing a specialized or dedicated controller. By leveraging the existing ElasticJob framework, we avoid unnecessary complexity while achieving accurate, quota-aware rollout behavior aligned with Kubernetes’ native mechanisms.

---

> For scale we just need to scale quota, I see no need for managing ReplicaSets

I agree, scale operations do not pose any additional requirements since scale-up and scale-down are already supported and don’t require any special handling for either Deployments or ReplicaSets, just as they don’t for `batchv1/Job`. This behavior is already well-covered by existing mechanisms and doesn’t introduce any additional complexity.

---

> the feature remains Alpha, and so Im not convinced it is good idea to already start pivoting designs in Kueue by that.

That’s a valid concern, and I agree we should be cautious about overcommitting to Alpha-level features.

That said, I wouldn’t characterize this as a pivot in design, rather, it’s an opportunity to **align early with emerging patterns** that are increasingly relevant, especially as we explore elasticity and fine-grained workload management.

By building support in a way that’s **feature-gated and modular**, we can evolve alongside the feature without locking ourselves in. It also allows us to provide early feedback and help shape the direction based on real-world usage, something Kueue is well-positioned to contribute to.

Also, I’m not 100% sure, but I don’t believe building on top of an Alpha feature is precedent-setting in Kueue. Is it? If there’s prior art, this might simply follow that pattern, assuming we keep the integration isolated and opt-in.

Of course, if the feature doesn’t mature as expected, we can always revisit or disable the integration cleanly without disrupting the broader system.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T08:24:16Z

Let me start from end:

> That said, I wouldn’t characterize this as a pivot in design, rather, it’s an opportunity to align early with emerging patterns that are increasingly relevant, especially as we explore elasticity and fine-grained workload management.

Yes, this is possible in principle. However, in this case 
1. I have other concerns about the proposal than just using alpha (see below), 
2. This is talking about adding new integration support (ReplicaSet) for which the graduation process is much trickier as it involves CRD changes, which are harder to graduate / withdraw later.

so I'm extra cautious. 

> Also, I’m not 100% sure, but I don’t believe building on top of an Alpha feature is precedent-setting in Kueue. Is it? If there’s prior art, this might simply follow that pattern, assuming we keep the integration isolated and opt-in.

I don't think we have prior work of adding feature beta or GA on top of Alpha, this is my concern, because by enabling new integration (ReplicaSet) we would need to extend the CRD, and extending CRD schema is not easy to version (I think). 

> Of course, if the feature doesn’t mature as expected, we can always revisit or disable the integration cleanly without disrupting the broader system.

We could make some disclaimers, but this is extra effort we haven't exercised in the past. Thus, I want to explore the option of adding workload at the Deployment level first.

> Respectfully, I have to fully disagree with the statement that "Deployment upgrades require the same amount of quota."

Indeed, I missed it totally. 

For StatefulSet we only support upgrades which don't modify the "pod template shape" (including resources and nodeSelectors) in [webhook](https://github.com/kubernetes-sigs/kueue/blob/ad32960f10f3477cafde0c28367aa4b169caff3c/pkg/controller/jobs/statefulset/statefulset_webhook.go#L159-L163), for shape definition check [here](https://github.com/kubernetes-sigs/kueue/blob/ad32960f10f3477cafde0c28367aa4b169caff3c/pkg/util/pod/pod.go#L119-L132). 

This is the most common upgrade scenario (for patch releases and some minor releases), but I agree the current support is not ideal. 

Now, we can make this work better with WorkloadSlices replacements by using two PodSets: "main"  and "replacement". The "main" is gradually decreasing while the "replacement" is increasing. This approach would be transferable between Deployments and StatefulSet. The good thing is that when "main" and "replacement" use same "pod template shape" we could merge them resulting in much less flopping of the quota size.

I think doing workload at the Deployment level has some advantages over ReplicaSet:
1. For the typical case of upgrading only image (patch release) we can pretty much keep constant quota, using fewer QPS requests than for managing two workloads. 
2. The extra context of "seeing" both ReplicaSets allows for quota management optimizations in case the PodTemplates don't differe
2. The solution can be almost directly transferred to StatefulSets
3. Managing 2 workloads, per ReplicaSets, may result in the upgrade getting stuck in a weird state when the "new" ReplicaSet workload is preempted while the "old" still has quota. Using single workload makes the preemption during upgrade atomic.
4. Does not extend the API surface to support ReplicaSets which seems unnecessary

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-04T22:13:17Z

> 2\. This is talking about adding new integration support (ReplicaSet) for which the graduation process is much trickier as it involves CRD changes, which are harder to graduate / withdraw later.

I don’t believe this involves any CRD changes.

ReplicaSet support would be implemented within the existing `jobframework` integration, similar to how we support other workload types like StatefulSet or Job. There's no need to introduce new API types or modify existing CRDs.

From Kueue's perspective, this is purely internal integration logic. So the graduation risk associated with CRD changes doesn’t apply in this case.

Let me know if I’m missing some specific implication you're referring to.

---

> I don't think we have prior work of adding feature beta or GA on top of Alpha,

Perhaps there’s a misunderstanding here. Since support for ReplicaSet/Deployment would itself be introduced as **Alpha**, there is no case of a Beta or GA feature depending on an Alpha one. This would be **Alpha on top of Alpha**, which, as I mentioned in my previous message, seems to follow an existing pattern in Kueue.

In fact, we already have Alpha features in Kueue that are built on top of other Alpha features. This effort would follow the same approach and doesn’t represent a departure from that precedent.

> because by enabling new integration (ReplicaSet) we would need to extend the CRD, and extending CRD schema is not easy to version (I think).

I’m not sure I entirely follow, could you clarify which CRD(s) you believe would need to be extended for ReplicaSet integration?

As far as I can tell (and as I mentioned above), there shouldn’t be any. This support would be added internally within the controller logic, without requiring changes to Kueue’s CRD schemas.

--- 

> Now, we can make this work better with WorkloadSlices replacements by using two PodSets: "main" and "replacement". The "main" is gradually decreasing while the "replacement" is increasing. This approach would be transferable between Deployments and StatefulSet. The good thing is that when "main" and "replacement" use same "pod template shape" we could merge them resulting in much less flopping of the quota size.


There’s a lot to unpack here, and I’m not sure I’m ready to do it justice in this format. One thing that does seem clear, though, is that there may be some misunderstandings (or misconceptions) around how native ReplicaSet/Deployment/StatefulSet support could be implemented in Kueue using ElasticJobs(via workload slices).

That, in itself, is a strong indication that a more detailed design proposal is warranted, so we can avoid making assumptions or drawing premature conclusions. As far as I’m aware, there should be no need for CRD changes, nor do I expect any "quota flopping", though I’m not entirely sure what that refers to in this context.

My concern is that rejecting this idea without fully understanding the technical details and the potential merits (or shortcomings) may be a bit premature. A KEP might be a good vehicle to flesh this out and allow us to evaluate it properly. What do you think?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T06:13:13Z

> I don’t believe this involves any CRD changes.

Actually, you are right, sorry for the confusion. 

> Let me know if I’m missing some specific implication you're referring to.

I was thinking about manifest changes as such, and usually when we add new integrations these are accompanied with new webhooks which are naturally blowing the diff and manifests. I'm not yet totally sure how dropping webhooks works on upgrade of Kueue, but we could probably figure this out.

> Perhaps there’s a misunderstanding here. Since support for ReplicaSet/Deployment would itself be introduced as Alpha, there is no case of a Beta or GA feature depending on an Alpha one. This would be Alpha on top of Alpha, which, as I mentioned in my previous message, seems to follow an existing pattern in Kueue.

Indeed, we could call it Alpha. The tricky part is versioning of webhooks, but we can just call them Alpha.

> In fact, we already have Alpha features in Kueue that are built on top of other Alpha features. This effort would follow the same approach and doesn’t represent a departure from that precedent.

Yes, this is ok.

> I’m not sure I entirely follow, could you clarify which CRD(s) you believe would need to be extended for ReplicaSet integration?

As above, sorry for confusion.

>  (...) I expect any "quota flopping", though I’m not entirely sure what that refers to in this context.

Here I meant that in case of Deployment upgrade, when both PodTemplates have some "pod template shape" I expect a lot more changes to the requested quota as one ReplicaSet is scaling down and the other is scaling up pretty much independently. This scenario with workload at the Deployment level can make quota requested quota as "old" + "new" which I expect is much more stable over time.

> My concern is that rejecting this idea without fully understanding the technical details and the potential merits (or shortcomings) may be a bit premature.

I don't want to reject idea of supporting Deployments via workloadSlices. I just want weigh the pros & cons of doing this at the ReplicaSet vs Deployment level. My gut feeling is that doing this at the Deployment is better for user experience and maintainability of Kueue. I acknowledge I might be missing something, but I expect also consider Deployment-level workload as a viable option.

> A KEP might be a good vehicle to flesh this out and allow us to evaluate it properly. What do you think?

Might be a KEP or even a Google Docs design doc focus just on compering both approaches.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-05T22:36:57Z

As the saying goes, *"a picture is worth a thousand words"*, so I decided to create a quick prototype for native Kueue `Deployment` support using ElasticJobs (WorkloadSlices) via `ReplicaSet`:

🔗 [https://github.com/ichekrygin/kueue/tree/replicasets](https://github.com/ichekrygin/kueue/tree/replicasets)

**EDIT:** Converted to a [DRAFT PR](https://github.com/kubernetes-sigs/kueue/pull/6475) to make it easier to review and provide feedback.

If you diff the code, you’ll see that all (functional) changes are localized to just three files:

* `replicaset/rs_controller.go`
* `replicaset/rs_webhook.go`
* `jobs/job.go`

The first two files contain basic scaffolding for the controller and webhook logic. It’s important to note that they don’t introduce any new functionality beyond what exists in the `jobs/job` package, these are essentially *reduced* versions of those analogs.

The third file simply registers the new integration framework.

The reason for such a minimal change footprint is that the heavy lifting is already handled by the existing workload-slicing implementation. Furthermore, the native `Deployment` → `ReplicaSet` lifecycle in Kubernetes is particularly well-suited to leverage WorkloadSlices. As a result, we’re able to deliver **full native Deployment support** in Kueue **without** adding any Deployment or ReplicaSet-specific logic.

🎥 I’ve attached a screen recording demonstrating the prototype with support for:

* Deployment scaling (including down to 0 replicas)
* Deployment updates (including changes to resource requests)

https://github.com/user-attachments/assets/c7d1c4e6-b513-4175-a747-149d01532a7f

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-05T23:14:00Z

> The solution can be almost directly transferred to StatefulSets

As suggested, I envision that adding full-spectrum native Kueue support for `StatefulSet` could follow the exact same pattern, with comparable complexity (or lack thereof). 

Moreover, with the [upcoming MultiKueue support for ElasticJobs](https://github.com/kubernetes-sigs/kueue/pull/6445), we’ll gain additional benefits, namely, native Kueue support for both `Deployments` and `StatefulSets` in the MultiKueue context.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-07T15:45:34Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T12:04:28Z

Ok, cool. I'm still not fully convinced if two workloads per ReplicaSets are better than one workload for Deployment. Mainly due to atomicity. 

However I acknowledge there are complications to use one workload at the Deployment level:
- managing two PodSets during update
- ungating Pods which are two level down from the Workload

Since ReplicaSets are essentially like batch Jobs I see why it is easier to get going with this approach.

So, since we may change plans in the future I'm ok to accept it as Alpha. Please just add a graduation point for Beta in KEP to reevaluate the approach. 

As for now it would be much better if we could eliminate the webhooks from ReplicaSet, because it will make the upgrade process easier in the future if we decide to change the approach.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-08T15:05:59Z

> So, since we may change plans in the future I'm ok to accept it as Alpha.

Fantastic! 🎉 

> Please just add a graduation point for Beta in KEP to reevaluate the approach.

Do you mean add this to the existing KEP-77, or should I create a new KEP?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T15:11:04Z

Existing

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-12T15:50:05Z

> Existing

Created #6564, PTAL @mimowo + et.al.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-10T16:29:09Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-10T17:22:33Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:24:12Z

/priority important-longterm
/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:22Z

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

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-08T16:16:30Z

In response to: https://github.com/kubernetes-sigs/kueue/pull/6475#issuecomment-4207445326

@mwielgus thanks, I think this is a very fair question.

Let me try to answer it directly, focusing specifically on **gang scheduling behavior** and when “8 is better than 5” is *not* the right outcome.

**First, what exists today**

Today, with pod-integration, there is no gang scheduling behavior for Deployment at all. Everything is per-Pod:

* scaling `5 → 10` with capacity for `8` results in:

  * 8 running Pods
  * 2 pending Pods
* effectively, the system always converges to “best effort”

There is no way to express: *“only proceed if I can get +5 as a unit”*.

**Second, what gang scheduling behavior changes**

With workload-level (ReplicaSet-based) semantics:

* scaling `5 → 10` is interpreted as a request for **+5 replicas as a unit**
* if capacity for all 5 is not available:

  * the new slice stays **Pending**
  * the system does **not** partially advance that step

This is the key semantic difference:
the scale step is treated as a **capacity commitment**, not a best-effort request.

**Now, your example: why not just go to 8?**

If the user *wants* to get to 8, they can express that directly:

* scale `5 → 8`
* or use smaller steps (`maxSurge`, HPA policy, imperative scaling)

In that case:

* the 9th replica would simply remain pending until capacity appears
* more importantly, this is represented as:

  * one admitted workload with 8 Pods
  * one pending workload with 1 Pod

So the system state is explicit and workload-oriented.

Contrast that with pod-integration:

* the same situation is represented as **9 independent workloads** (one per Pod)

At small scale this looks equivalent, but at realistic scale it diverges quickly:

* 2 workloads vs 9
* or 2 vs 90
* or 2 vs 900

This is not just cosmetic, it directly affects:

* control plane load
* reconciliation cost
* clarity of admission state (one logical step vs many independent fragments)

**So when is “8 is better than 5” *not* true?**

The key case is when the user intent is not “give me whatever you can”, but:

> “this scale step only makes sense if it completes as a whole”

Examples:

* the additional replicas represent a **new capacity tier** (e.g., handling a traffic class, enabling a feature, opening shards)
* partial scale introduces **inconsistent or misleading state** (system appears scaled, but does not actually meet requirements)
* the user wants **explicit backpressure** instead of silent degradation

In those cases, going to 8 is not actually “better”, it is just **silently different from what was requested**.

---

**Summary**

* pod-integration → always best-effort, per-Pod (no gang semantics)
* ReplicaSet-level → allows **gang scheduling behavior per scale step**
* elastic behavior is still fully possible, but must be **expressed explicitly by the user**
* workload-level modeling reduces fragmentation (2 workloads vs N Pods), which becomes significant at scale

So the question is not whether 8 can be better than 5, it often is.
The question is whether the system should *always* make that choice implicitly, or allow users to express when it should not.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-08T18:00:46Z

In response to and as a follow-up discussion for: https://github.com/kubernetes-sigs/kueue/pull/6475#issuecomment-4204416072


I think the core of this discussion is not really **workload:Deployment vs workload:ReplicaSet** as competing UX models, but rather:

**what is the correct abstraction boundary that allows Kueue to support Deployment semantics given its current mutability model?**


### 1. The real constraint: Kueue is (still) largely immutable

Historically, Kueue workloads follow a **replace, not update** model:

* any change affecting resource shape → new Workload
* existing Workload is not meaningfully mutated

There are limited exceptions (e.g. StatefulSet), but only for **non–resource-shape changes** (image, metadata). That is not true mutability, it is a constrained compromise.

This is still true today.

The only real step forward is **ElasticJobs / WorkloadSlices (KEP-77)**, which allow controlled replacement, not general in-place mutation.


### 2. Why Deployment suddenly works

This PR does not succeed because Kueue gained mutability.

It succeeds because **Deployment already externalizes mutation**:

* **scale** → updates `.spec.replicas` on the same ReplicaSet
* **update** → creates a *new ReplicaSet*

This is critical.

Kueue does not need to solve mutability for Deployment, Kubernetes already did it.

So instead of inventing new semantics, we can directly map:

* ReplicaSet → Workload
* scale → existing behavior
* update → natural replacement via new ReplicaSet

That is why `workload:ReplicaSet` is not arbitrary, it is the **native mutation boundary** defined by Kubernetes.

### 3. Why this is actually the simplest path

The key property that makes Deployment work here is not universally present across other integrations.

In particular:

* **StatefulSet** does not externalize mutation into separate objects, so Kueue must restrict updates to avoid changes in workload shape
* **LWS / ElasticJobs** introduce Kueue-specific abstractions (e.g., slicing, replacement, and cross-workload coordination), requiring Kueue to manage additional lifecycle and consistency semantics

In contrast, **Deployment already separates mutation from scaling via ReplicaSets**, providing a natural boundary that Kueue can directly reuse.

This is what makes Deployment uniquely well-aligned with Kueue’s current model and allows for a simpler implementation without introducing new mutation semantics or coordination logic.


### 4. Complexity: where it actually lives

The key difference is not the *amount* of code, but the *type* of complexity.

**StatefulSet integration:**

* must restrict mutability
* must define and validate “pod template shape”
* must prevent unsupported transitions
* must encode rollout assumptions inside Kueue

→ complexity = **policy + validation + constraints**

**Deployment + ReplicaSet integration:**

* no mutation rules required
* no shape validation needed
* no rollout logic implemented in Kueue
* relies on Kubernetes-native behavior (new RS on update, scaling semantics)

→ complexity = **observation + mapping**

Put differently:

> StatefulSet requires Kueue to *define and enforce* mutation rules, while Deployment+ReplicaSet simply *observes and maps* mutation already expressed by Kubernetes.

This is also reflected in the implementation, where the functional changes are minimal and most of the behavior is reused from existing workload-slicing logic.

### 5. MultiKueue concern (valid, but scoped)

This is a fair concern, but it’s important to ground it in the current state.

Today, there is **no meaningful MultiKueue support for Deployment** beyond pod-integration, which itself does not provide workload-level semantics. So we are not regressing an existing, well-defined model.

Given that, there are three possible directions:

**A. Introduce true mutable workloads in Kueue**
This would allow Deployment-level modeling directly, but requires adding a capability Kueue does not have today. This is the highest-cost option.

**B. Restrict Deployment mutability (StatefulSet-style)**
Limit updates to non–resource-shape changes to fit the current model. This is lower cost, but it effectively removes key Deployment semantics.

**C. Use ReplicaSet as the propagation unit**
Leverage the existing Deployment → ReplicaSet lifecycle. This preserves full semantics while requiring minimal new logic.

Given that:

* single-cluster support already works with (C), and does so naturally
* MultiKueue support for Deployment is not yet defined

→ **(C) is the most practical and lowest-risk option to build on**

The key question then becomes:

> Why must Deployment itself be the propagation unit?

Requiring that constraint implicitly forces us back into a limited mutability model, because Deployment does not expose a clean mutation boundary. In contrast, ReplicaSet already provides that boundary, which is exactly what enables a correct and minimal implementation.

### 6. UX argument

Concern: bReplicaSet-level workloads may be confusing vs Deployment.

But today we already have: **Deployment → ReplicaSet → Pod**

And we support: **workload:Pod** 

If ReplicaSet is “too low-level”, Pod is even further removed from user intent. Yet pod-integration is accepted.

ReplicaSet is actually the **first level that preserves rollout semantics**. Pods do not.

So from a UX perspective:

* Pod-level → fragmented, least aligned
* ReplicaSet-level → coherent rollout unit
* Deployment-level → ideal, but requires mutability Kueue does not have

### 7. Summary

* Kueue does not support general mutable workloads

* Deployment works because Kubernetes externalizes mutation via ReplicaSets

* ReplicaSet is the natural and lowest-cost workload boundary

* Deployment-level workloads require either:

  * new mutability support (high cost), or
  * reduced semantics (StatefulSet-style)

* MultiKueue does not currently constrain this decision

* ReplicaSet-level modeling is:

  * simpler in implementation
  * aligned with Kubernetes rollout semantics
  * less fragmented than pod-level integration

---

**Conclusion**

ReplicaSet is not being introduced as a UX abstraction.

It is being used because it is the **only abstraction that allows full Deployment semantics within Kueue’s current architecture**, without introducing new mutability primitives or degrading behavior.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-09T07:50:25Z

> 1. The real constraint: Kueue is (still) largely immutable
> (...)
> The only real step forward is ElasticJobs / WorkloadSlices (KEP-77), which allow controlled replacement, not general in-place mutation.

Agree, the competing proposal, Deployment-level Workload, is also based on top of WorkloadSlices, just making 1:1 correspondence between the user Workload Deployment, and Kueue's Workload.

On complexity:

> 3. Why this is actually the simplest path
> 4. Complexity: where it actually lives

I think using the ReplicaSet for the basis of Workload has many hidden complexities, which are currently not covered in the PR, and I'm concerned they will be necessary later if we choose this path.  In particular, it remains unclear to me how and where we are going to ensure the two Workloads land on the same ResourceFlavor. 

The problems stem from the fact that the two ReplicaSet workloads are completely independent (not even the same Workload slice), so additional coordination will be needed and scattered across the codebase.

They would not be necessary if we choose a Deployment-level workload. This code to ensure Workloads which belong to the same WorkloadSlices land on the same ResourceFlavor already exists Deployment level it would fall naturally.

> 5. MultiKueue concern (valid, but scoped)

Again, I think the best option is to use Deployment-level Workload. We decided that approach in the context of all other integrations. For example in the context of RayJob we tried initially with RayCluster (child job) hoping this is less work, but then it turned out to be really tricky wrt RaySubmittedJob.Similarly we need to sync entire RayService so that the Gateways are created on the Worker cluster.

I don't like the idea of re-discovering the wheel for MultiKueue per integration. The syncing of the top-level user-workload is the simplest model here IMO.

> 7. Summary
> It is being used because it is the only abstraction that allows full Deployment semantics within Kueue’s current architecture, without introducing new mutability primitives or degrading behavior.

Here I have a different mental model. First, full Deployment semantics is already provided by the Pod-based integration (without gang scheduling which is unusual for Deployments anyway). 
Second, if we need gang scheduling for Deployments then I think Deployment-level workload is the path to go, and it could also support full mutability. I don't see how Kueue's architecture would be getting "in the way" here.

Actually, given so different mental models I think this PR really needs to be first go via KEP cycle. I would also want to look for some assignee to try the Deployment-level approach. Again, I admit I might be wrong, but I think we shouldn't dismiss this option just because it wasn't prototyped yet. In my mental model it aligns with Kueue architecture much cleaner.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-09T16:04:09Z

Thanks for the thoughtful discussion, I think we’re getting closer to the core of the disagreement.

Let me try to reframe the problem from a slightly different angle.

### The core gap: lack of workload mutability

Today, Kueue does not have meaningful support for **workload mutability**.

Workloads are effectively immutable with respect to workload shape:

* changes to resources, placement, or pod template → treated as replacement
* limited exceptions exist, but only for non–resource-shape updates

WorkloadSlices (ElasticJobs) help with **replacement and scaling**, but they do not provide general mutability. They allow us to model *multiple workloads over time*, not to evolve a single workload in place.

### Why this matters for Deployment-level Workload

A `Deployment → Workload` model fundamentally assumes that a single logical workload can evolve across updates.

That requires:

* representing both “old” and “new” states within a single workload
* coordinating quota between those states
* defining transition semantics during rollout

Today, Kueue does not provide primitives for this.

So even if we use WorkloadSlices, we are still left with the same question:

> where and how is mutation actually modeled?

Slices address replacement and scaling, but they do not solve:

* in-place evolution of workload shape
* unified accounting across versions
* rollout coordination within a single workload

### ReplicaSet-based approach as a fit for current model

Given that constraint, the ReplicaSet-based approach works well because it aligns with the existing Kueue model:

* Kubernetes externalizes mutation via new ReplicaSets
* old and new states are already separated
* Kueue can map each ReplicaSet to a Workload
* no new mutability semantics are required

This is not claiming it is perfect, it has trade-offs, but it works **within the capabilities Kueue has today**.

### On complexity and coordination concerns

Concerns around coordination (e.g., ResourceFlavor alignment) seem to fall into **policy**, not correctness.

* flavor stickiness is something we already handle today
* Kubernetes does not require ReplicaSets within a Deployment to share identical placement
* updates can legitimately change resource shape or placement constraints

If users require consistent placement, that can be expressed via:

* pod-level constraints (nodeSelector / affinity)
* or higher-level policy (e.g., flavor stickiness), which we already support and can extend

So I don’t see this as a missing invariant that blocks the ReplicaSet-based approach.

### Path forward

I want to emphasize that I’m fully supportive of a `Deployment → Workload` model.

However, I think the correct path to get there is:

1. Introduce **workload mutability** as a first-class concept in Kueue
2. Define how mutation, rollout, and quota coordination are handled
3. Build Deployment-level workload support on top of that

Without that foundation, it’s difficult to see how Deployment-level Workload can be implemented correctly using existing primitives alone, including WorkloadSlices.

### On KEP vs PR scope

Given the different mental models, I agree that a more structured comparison could be useful.

However, I don’t think this PR itself requires going through a KEP:

* it does not introduce new primitives
* it does not change the workload model
* it operates fully within the current replace-oriented semantics

This is also consistent with how we’ve extended WorkloadSlices to other integrations (e.g., Job, Ray), by reusing existing mechanisms rather than introducing new abstractions.

In contrast, a Deployment-level Workload approach appears to depend on **workload mutability**, which is not currently part of Kueue.

Introducing mutable workloads would be a broader architectural change affecting multiple integrations, and that is where I would expect a KEP (or design doc) to be the right vehicle.

### Summary

* WorkloadSlices address replacement and scaling, not general mutability
* Deployment-level Workload requires mutability semantics that Kueue does not yet provide
* ReplicaSet-based modeling works with the current replace-oriented model
* Adding workload mutability would unlock a cleaner Deployment-level approach

So from my perspective:

> ReplicaSet-based Workload is the best fit for the current architecture,
> and workload mutability is the right next step to enable Deployment-level Workload in the future.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-09T16:18:35Z

> Thanks for the thoughtful discussion, I think we’re getting closer to the core of the disagreement.

Agree, let me try to get deeper into this particular bit which I have a different mental model on: 

> However, I think the correct path to get there is: Introduce workload mutability as a first-class concept in Kueue

In the approach Im trying to put forward the "workload" mutability is not needed to allow Deployment mutability. 

The changes in the Deployment are reflected by new WorkloadSlices created by the deployment controller. Let me give an example:

1. steady state Deployment with size 5, has one one Workload1 :replica-1: 5" (replica-1 is PodSet name, 5 is size)
2. as the rolling update is progressing we have Workload2: "replica-1: 4", "replica-2: 1" -> "replica-1:3", replica-2: 2" ->... ->  replica-2: 5"
3. we reach the new steady state with Workload6 with one PodSet :"replica-2: 5"

wdyt?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-10T02:37:26Z

Thank you for the alternative design suggestion, it is interesting. Let me restate my understanding to make sure I’m following correctly.

As I understand it:

* a Deployment maps to a single, top-level Workload
* ReplicaSet versions are represented as PodSets within that Workload
* rollout is modeled by adjusting PodSet sizes (old shrinking, new growing)
* WorkloadSlices remain orthogonal admission/scaling units and may carry updated PodSets, but do not define rollout semantics

So rollout state is effectively encoded inside a single Workload via multiple PodSets.

---

Given that, I see a few core concerns.

**1. PodSet semantic mismatch**
PodSets represent parallel roles today. Using them to encode temporal versions (old/new ReplicaSets) mixes orthogonal concerns and changes their meaning.

**2. Implicit semantics**
Since versioning is not part of the API, this relies on conventions (labels/names) to distinguish PodSets, which the scheduler and controllers must interpret.

**3. Scheduler impact**
The scheduler would need to distinguish active vs transitional PodSets and selectively account for them, effectively becoming rollout-aware.

**4. No mutability support**
Workloads are largely immutable today. This model introduces evolving workload state (multiple versions, transitions) without explicit primitives to support it.

**5. Continuous updates and coupling**
Workload would need to be updated continuously as ReplicaSets scale, tightly coupling Kueue to rollout progress and increasing control-plane churn.

**6. Loss of clear boundaries**
The clean “scale vs update” signal provided by ReplicaSets is lost, requiring Kueue to infer rollout semantics from PodSet diffs.

**7. State reconstruction**
The controller would need to observe Deployment/ReplicaSets (and possibly Pods) to reconstruct rollout state, duplicating logic already in Kubernetes.

**8. Multi-ReplicaSet scenarios**
Real deployments can have multiple ReplicaSets (failed rollout, rollback, retry), leading to multiple PodSets and unclear lifecycle/admission semantics.

**9. Limited generality**
This approach is inherently tailored to single-template, mutable workloads (e.g., Deployment, StatefulSet), and does not generalize to multi-template workloads (e.g., RayCluster, LWS), while also being inapplicable to non-mutable workloads such as v1.Job.

**10. Loss of atomicity**
A Workload becomes an evolving structure rather than a stable scheduling unit, pushing lifecycle concerns into Kueue.

---

I do see the value in a top-level, user-facing Workload for Deployment.

However, overloading PodSets for rollout/version semantics does not seem like a good fit. If we want a true `Deployment -> Workload` mapping, a more principled direction might be **hierarchical workloads**:

* parent Workload for user intent
* child Workloads as scheduling units (e.g., per ReplicaSet)
* parent aggregates status

The concurrent workload admission work could be a good starting point or reference for this direction.
Notably, the ReplicaSet-based approach already aligns well with this model.


At any rate, I don’t see this approach resulting in a smaller or simpler change than the current PR. If anything, it introduces additional complexity across multiple areas.

From my perspective:

* the ReplicaSet-based approach aligns with the current model and Kubernetes semantics
* the proposed Deployment-level approach requires new capabilities (mutability, rollout coordination, scheduler changes)

and definitely warrants a more explicit design effort rather than being encoded via PodSets.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-13T16:22:36Z

Folks, one more thought I had recently. While we should proceed with KEP for making this integration part of the core Kueue I will be supportive to make it as an addon integration incubated under cmd/experimental. 

This would let us unblock some immediate use cases, while addressing my concerns about leaking the integration to core webhooks and Config API. Then we could have all the time in the world to collect use cases and properly design the integration before incorporating into the core Kueue.

For the technical level pointers, I imagine the closest would be [kueue-populator](https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental/kueue-populator). Also in the past we had such addon integration for [tains&tolerations](https://github.com/kubernetes-sigs/kueue/tree/release-0.9/cmd/experimental/podtaintstolerations). This could also serve as an example to how to write an in-house integration which we currently don't have.
