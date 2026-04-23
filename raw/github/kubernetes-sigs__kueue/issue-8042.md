# Issue #8042: MultiKueue via ClusterProfile: Standardize credentials plugins distribution

**Summary**: MultiKueue via ClusterProfile: Standardize credentials plugins distribution

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8042

**Last updated**: 2026-03-19T08:59:59Z

---

## Metadata

- **State**: open
- **Author**: [@hdp617](https://github.com/hdp617)
- **Created**: 2025-12-02T21:39:24Z
- **Updated**: 2026-03-19T08:59:59Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
MultiKueue with ClusterProfile API requires a credentials plugin to be available to the kueue manager (see [KEP-5993](https://github.com/kubernetes/enhancements/blob/master/keps/sig-multicluster/5339-clusterprofile-plugin-credentials/README.md)). Currently, there is no standardized way to distribute these plugins. This enhancement request aims to standardize the method for distributing and making cloud-provider credential plugins available to the kueue manager.

### Proposed Options

#### Option 1: Include the plugins in the Kueue Manager container image
* **Option 1A: Plugins Built and Managed by Kueue**. Plugins (e.g., for AWS, GCP, Azure) are compiled and included directly in the official Kueue manager container image, similar to [Argo CD](https://github.com/argoproj/argo-cd/tree/master/cmd/argocd-k8s-auth/commands).
    * **Pros:** Offers the best UX as it requires zero extra configuration from the user.
    * **Cons:** Introduces cloud-provider specific logic in kueue - this might be acceptable as there's prededence from Argo CD and the provider-specific logic is limited to auth.

* **Option 1B: Plugins Built and Managed by Customers**. Customers are responsible for compiling and building a custom Kueue manager image that includes their required credential plugins.
    * **Pros:** Keeps cloud-specific logic out of the main Kueue repository.
    * **Cons:** High friction for users, requiring them to maintain a custom build pipeline.

#### Option 2: Provide the plugins at run time
Plugins are provided at run time, typically via an **`initContainer`** that mounts them into the Kueue manager's volume.
 * **Pros:** Decouples the plugin lifecycle from the Kueue manager release cycle.
 * **Cons:** Adds complexity to the deployment manifest as it requires an `initContainer`, volume mounts, etc. It also requires maintaining container images for the plugins -  it would be useful to have the plugins hosted in a k8s repos and shared among multi-cluster toolings.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-02T21:40:40Z

cc @mimowo @zhang-xuebin @knee-berts

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T07:47:28Z

I think both should be provided since hosting plugins for major cloud providers by the upstream Kueue controller-manager would be really useful. The cluster admin just installed kueue the same as today.

OTOH, I think that we should open an interface for on-prem or minor regional cloud providers.

At the first step, we can work for the major cloud providers (Google Cloud?).

> Plugins are provided at run time, typically via an initContainer that mounts them into the Kueue manager's volume.

I'm not familiar with the ClusterProfile mechanism, but can we host such a mechanism in another Pod? Because we have some of the extensible interfaces like JobFramework, AdmissionChecks, MKDispathcers which typically are implemented in another Por rather than upstream kueue-controller-manager.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T07:51:46Z

I have added a related topic to the agenda for the next wg-batch (Dec 4th). 

While I think it makes sense to provide the plugins along with Kueue for the ease of deployment, I would prefer not to need to compile or maintain them. Just use them as a dependency on the image built by some centralized repository for the plugins. This would also allow to deduplicate the implementations for the plugins with argo-cd. 

I think such plugins could be built and published as images by the https://github.com/kubernetes-sigs/cluster-inventory-api project, similarly is Kueue is publishing images.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T07:51:52Z

@kannon92 Could you share if we should implement Openshit dedicated credential mechanism for MultiKueue? Or does Openshit rely on any standardized credential mechanism?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T08:02:52Z

> I think such plugins could be built and published as images by the https://github.com/kubernetes-sigs/cluster-inventory-api project, similarly is Kueue is publishing images.

If cluster-inventory-api could manage plugins, it would be better, I think.

### Comment by [@qiujian16](https://github.com/qiujian16) — 2025-12-04T14:26:31Z

>I'm not familiar with the ClusterProfile mechanism, but can we host such a mechanism in another Pod? Because we have some of the extensible interfaces like JobFramework, AdmissionChecks, MKDispathcers which typically are implemented in another Por rather than upstream kueue-controller-manager

The required plugin is a bin that can be executed in kubeconfig. One way is to start a init container and copy the plugin binary to the volume that kueue manager can mount later. Or I think it is possible to directly mount image with plugin as volume today.

I remember the previous discussion on cluster-inventory-api is it will not maintain plugins for different vendors. But I think it worth a discussion to at least document how to use the plugin. cc @corentone

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-04T15:16:02Z

Yes, I think it will be possible to mount the plugin directly using the `ImageVolume` feature which is going to be enabled by default in [1.35](https://github.com/kubernetes/kubernetes/blob/615ac0d2996f36fe4df7410e1168a8577e7045ba/pkg/features/kube_features.go#L1369)

### Comment by [@corentone](https://github.com/corentone) — 2025-12-10T11:13:34Z

I wasn't aware of the ImageVolume but this is a great suggestion. Thanks @mimowo 
That way the plugin can have its own lifecycle (and be separately open sourced) while avoiding configmap limitations!

Indeed, Cluster Inventory will not manage plugins. I think the different providers should publish images (I am [suggesting to make this the official way](https://kubernetes.slack.com/archives/C09R1PJR3/p1765364493560949) of mounting the plugins!).

For example, Google would publish an image that contains the necessary plugin. (We will likely have to provide a gcloud-free version of the plugin image or find a way for the plugin to use the volume-mounted gcloud instead of $PATH)

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-11T13:11:21Z

https://github.com/kubernetes/enhancements/pull/5354

I'm not sure ImageVolume will support this anymore.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-11T13:27:54Z

> [kubernetes/enhancements#5354](https://github.com/kubernetes/enhancements/pull/5354)
> 
> I'm not sure ImageVolume will support this anymore.

AFAIK, the binary mounted via image volume could be executed. In the initial KEP, they were planning to enforce the `noexec` option. But, after some discussions, they decided to allow us to mount the OCI image as an exec option.

> 06-17-2025 KEP retargeting beta in v1.34, dropped noexec requirement

https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/4639-oci-volume-source/README.md#implementation-history

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:19:59Z

/area multikueue
/priority important-soon

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:20Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T08:59:58Z

/remove-lifecycle stale
