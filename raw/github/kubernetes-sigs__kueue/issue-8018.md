# Issue #8018: Use v1beta2 as storage for 0.16

**Summary**: Use v1beta2 as storage for 0.16

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8018

**Last updated**: 2026-01-23T07:18:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-01T12:14:58Z
- **Updated**: 2026-01-23T07:18:05Z
- **Closed**: 2026-01-23T07:16:22Z
- **Labels**: `priority/important-soon`, `kind/api-change`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 39

## Description

As we have 0.15 released which introduced v1beta2 for serving, the next step is to use v1beta2 for storage.

We can already prepare the PR.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T12:15:16Z

/kind api-change
/remove-kind cleanup

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-01T12:50:04Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T10:02:07Z

I think the remaining task here is to make sure we communicate to users that after installing 0.16 they should make sure all objects migrate to v1beta2. One idea is to use kubectl annotate to add some annotation to all objects.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-02T10:26:23Z

Or use kubectl-convert 
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-convert-plugin
- https://kubernetes.io/docs/reference/using-api/deprecation-guide/#migrate-to-non-deprecated-apis

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-02T10:50:52Z

> Or use kubectl-convert
> 
> * https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-convert-plugin
> * https://kubernetes.io/docs/reference/using-api/deprecation-guide/#migrate-to-non-deprecated-apis

I tested it – it doesn’t work. Looks like it only supports core Kubernetes resources.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T15:05:58Z

Ok, it is enough to specify the migration steps. Please update https://github.com/kubernetes-sigs/kueue/pull/8020#issue-3680831174 to make sure the steps are clear, and with example script which can do it reliably after the installation.

Please also send a PR to mark v1beta1 as deprecated in 0.16

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-14T03:57:37Z

Is this issue complete?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:43:32Z

/priority important-soon

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-09T14:08:39Z

### Migrating Kueue Resources to API Version `v1beta2`

Kueue plans to make `v1beta2` the primary storage version in v0.16. Support for `v1beta1` will end in later releases: `served=false` in ~v0.17~ v0.18 (no new resources can be created with `v1beta1`) and complete removal in ~v0.18~ v0.19.

The migration only updates the `apiVersion` field in existing Kueue custom resources to `kueue.x-k8s.io/v1beta2`. Kueue's conversion webhooks automatically handle any structural differences. The change is safe and affects only the stored version.

Run the migration after upgrading Kueue to the v0.16.

#### Steps

1. Download the official migration script:

   ```bash
   curl -O https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh
   chmod +x migrate-to-v1beta2.sh
   ```

2. Execute the script:

   ```bash
   ./migrate-to-v1beta2.sh
   ```

   - The script automatically detects and migrates all relevant Kueue resources (namespaced and cluster-scoped).
   - It requires `kubectl` access with permissions to patch Kueue CRs.
   - Progress and completion are displayed in the output.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T18:15:11Z

@mbobrovskyi thank you for the scripting under https://github.com/kubernetes-sigs/kueue/pull/8428. This generally makes sense, but we need to double test that at scale, at 100k workloads or so.  

I think the common way of bypassing the problem is using `--chunk-size` for kubectl get. 

Please try to investigate if this script allows us to process 100k objects.

EDIT: actually, I'm not sure, maybe it will work OOTB if kubectl supports pagination, but then the question is about memory at the client side. It would be good to test some reasonable scale like 10k at least first to see if this works well.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-16T17:10:01Z

> Please try to investigate if this script allows us to process 100k objects.

I tested locally with 10k objects. It works.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T17:23:35Z

Thank you for checking! I also synced with @mbobrovskyi that it took 15min, so I expect for large cluster it might be something like 1h (10x more workloads, but faster backend). 

So, I would propose to add some logging of he progress, like every 1000 items output the percent done, say `processed: 1000/100000 (1%)`. 

EDIT: however it is just a nice-to-have. I'm ok to just add a note that the script may take long on large clusters.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-16T21:45:20Z

I don't know if we can drop serving v1beta1 in 0.17.

From the [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/):

> GA API versions may be marked as deprecated, but must not be removed within a major version of Kubernetes
Beta API versions are deprecated no more than 9 months or 3 minor releases after introduction (whichever is longer), and are no longer served 9 months or 3 minor releases after deprecation (whichever is longer)

So my understanding is that in 0.16 we deprecated v1beta1, I think that means we have 9 months to keep v1beta1 around before we remove serving that API.

cc @everettraven who pointed this policy to me.

I think we should not drop serving v1beta1 in 0.17. This is too fast for users to migrate.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-17T06:56:01Z

> I don't know if we can drop serving v1beta1 in 0.17.
> 
> From the [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/):
> 
> > GA API versions may be marked as deprecated, but must not be removed within a major version of Kubernetes
> > Beta API versions are deprecated no more than 9 months or 3 minor releases after introduction (whichever is longer), and are no longer served 9 months or 3 minor releases after deprecation (whichever is longer)
> 
> So my understanding is that in 0.16 we deprecated v1beta1, I think that means we have 9 months to keep v1beta1 around before we remove serving that API.
> 
> cc [@everettraven](https://github.com/everettraven) who pointed this policy to me.
> 
> I think we should not drop serving v1beta1 in 0.17. This is too fast for users to migrate.

This issue doesn't aim to remove the v1beta1 API, AFAIK. We will just switch the storage version to v1beta2 in v0.16.0.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-17T12:26:33Z

> served=false in v0.17 (no new resources can be created with v1beta1) and complete removal in v0.18.

I think Kevin meant my comment here.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-18T09:25:29Z

> > served=false in v0.17 (no new resources can be created with v1beta1) and complete removal in v0.18.
> 
> I think Kevin meant my comment here.

AFAIK, they can still create v1beta1 resources, but those will be converted to v1beta2 resources and then stored in etcd as v1beta2, isn't it?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-18T09:40:13Z

In 0.16, we will move `storage=true` to `v1beta2`. After that, users will still be able to create `v1beta1` resources, and they should be automatically converted – right?

However, before removing `v1beta1` in 0.17 (as we previously discussed), I think we should first set `served=false`. This would mean users can no longer create new `v1beta1` resources, while any existing ones remain in etcd in case someone missed the conversion.

Only after that should we remove `v1beta1` entirely. I think this approach is much better than removing `v1beta1` directly, but I’m okay with postponing it to later releases if needed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-18T09:54:45Z

> In 0.16, we will move `storage=true` to `v1beta2`. After that, users will still be able to create `v1beta1` resources, and they should be automatically converted – right?
> 
> However, before removing `v1beta1` in 0.17 (as we previously discussed), I think we should first set `served=false`. This would mean users can no longer create new `v1beta1` resources, while any existing ones remain in etcd in case someone missed the conversion.
> 
> Only after that should we remove `v1beta1` entirely. I think this approach is much better than removing `v1beta1` directly, but I’m okay with postponing it to later releases if needed.

I see. I previously agreed to use v1beta2 as a storage version in 0.16, but I don't remember the discussion about `served=false`. If you can share the discussion or a link, it would be helpful.

I'm with @kannon92 that `served=false` should be avoided in v0.16. We always respect the API deprecation policy as much as possible, as we have committed to in the community.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-18T09:58:52Z

> I'm with @kannon92 that served=false should be avoided in v0.16. We always respect the API deprecation policy as much as possible, as we have committed to in the community.

I agree with that as well. This is my plan for future releases: https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3729056171.

In this plan, we set `storage=false` for `v1beta1` in 0.16 and `served=false` for `v1beta1` in 0.17. If you think we should postpone setting `served=false` for `v1beta1`, just let me know and I’ll update the comment.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-18T10:13:55Z

OK. As I can see from the deprecation documentation, we should keep an API version for three minor releases after deprecation. We deprecated `v1beta1` in 0.15, right? That would mean we can set `served=false` for `v1beta1` in 0.18 and completely remove `v1beta1` in 0.19.

@kannon92 @tenzen-y @mimowo – are you OK with this plan?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-18T10:14:50Z

Also, @kannon92 and @everettraven, thanks for pointing this out 🙏

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-18T13:21:10Z

The deprecation policy does say 9 months or 3 minor releases and pick the longer one. For Kueue, that may mean 4 minor releases.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T09:22:22Z

So, in that case, we can set `served=false` for `v1beta1` in 0.19 and completely remove v1beta1 in 0.20, right?

@tenzen-y @mimowo are you OK with that?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T10:47:51Z

I'm not opposed to that, but maintaining `v1beta1` until 0.19 feels long for a fast moving project like Kueue. So, I'm not sure following the core k8s policy in this particular case is the best approach.  I think we may need to discuss that more on the wg-batch. 

Even if we decide to discontinue v1beta1 in 0.19 or 0.20 I think for the release note in 0.16 we don't
I need to commit to a specific timeline, so I would suggest relaxing the messaging from: https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3729056171 

Maybe something like:
```
Migrating Kueue Resources to API Version v1beta2

Kueue v0.16 starts using `v1beta2` API version for storage. Consequently, all new Kueue objects created
after the upgrade will be stored using `v1beta2`. 

However, existing objects are only auto-converted to the new storage version by Kubernetes during a write
request. This means that Kueue API objects that rarely receive updates - such as Topologies, ResourceFlavors,
or long-running Workloads - may remain in the older `v1beta1` format indefinitely.

Ensuring all objects are migrated to `v1beta2` is essential for compatibility with future Kueue upgrades.
We tentatively plan to discontinue support for `v1beta1` in version 0.18.

To ensure your environment is consistent, we recommend running the following migration script after
installing Kueue v0.16 and verifying cluster stability. The script triggers a "no-op" update for all existing
Kueue objects, forcing the API server to pass them through conversion webhooks and save them in
the `v1beta2` version.

This change is safe, metadata-only, and affects only the stored version of the resources.
```
wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T11:18:32Z

> I'm not opposed to that, but maintaining v1beta1 until 0.19 feels long for a fast moving project like Kueue. So, I'm not sure following the core k8s policy in this particular case is the best approach. I think we may need to discuss that more on the wg-batch.

I have no strong opinion here. I'm ok with either 3 minor releases or 9 months. If @kannon92 is confident that we should keep v1beta1 for 9 months, and he can describe the actual scenario, I will probably be in favor of 9 months rather than 3 minor releases.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-19T17:02:42Z

If we diverge from the Kubernetes API support policy then we should draft our own statement on what we guarantee for support.

Right now we say we follow Kubernetes API deprecation policy. https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#production-readiness-status

https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3767678919

We should/can announce that v1beta1 is deprecated so that gives people notice that it will be dropped in a future release.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T17:10:52Z

> If we diverge from the Kubernetes API support policy then we should draft our own statement on what we guarantee for support.
> 
> Right now we say we follow Kubernetes API deprecation policy. https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#production-readiness-status
> 
> [#8018 (comment)](https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3767678919)
> 
> We should/can announce that v1beta1 is deprecated so that gives people notice that it will be dropped in a future release.

Kueue respects Kubernetes API policy, but doesn't guarantee to completely follow the policy.
Kueue used to break the policy if we can really justify breaking the policy.

So, my question to the community is whether there is any justification to ignore the API policy at this time, which could speed up Kueue development, but it might be unexpected behavior for users.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T17:13:19Z

> We should/can announce that v1beta1 is deprecated so that gives people notice that it will be dropped in a future release.

What is your expected platform to inform users of the deprecation?
We have already announced in v0.15.0 release note: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0
Any other recommendations?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T17:28:48Z

Note that the policy also leaves room for Exceptions in some cases: https://kubernetes.io/docs/reference/using-api/deprecation-policy/#exceptions:

No policy can cover every possible situation. This policy is a living document, and will evolve over time. In practice, there will be situations that do not fit neatly into this policy, or for which this policy becomes a serious impediment. Such situations should be discussed with SIGs and project leaders to find the best solutions for those specific cases, always bearing in mind that Kubernetes is committed to being a stable system that, as much as possible, never breaks users. Exceptions will always be announced in all relevant release notes

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-19T17:35:05Z

> > We should/can announce that v1beta1 is deprecated so that gives people notice that it will be dropped in a future release.
> 
> What is your expected platform to inform users of the deprecation? We have already announced in v0.15.0 release note: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0 Any other recommendations?

Right now, we are honestly struggling to keep up with Kueue releases.

Our 1.2 release was based on 0.14. We are hoping to have 1.3 in late Feb/March so that will probably be 0.16.

In our case we should be fine as 0.16 will have both v1beta1 and v1beta2 available. 

But 3 months is really short timeframe for enterprise users.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T17:38:25Z

but 0.17 will also have v1beta1. Iiuc we are hesitating now about 0.18 vs 0.19

### Comment by [@everettraven](https://github.com/everettraven) — 2026-01-19T17:59:09Z

Chiming in as I've been mentioned a couple times :)

@kannon92 reached out to me to talk about the semantics of removing a version from a CRD and I shared some links and thoughts with him - one of which was that since Kueue is a kubernetes-sigs project, you may want to take into consideration the Kubernetes API deprecation policy.

You certainly do not have to follow it to a T, but I would recommend that you follow a multi-release deprecation approach. In general, that looks something like:
- `0.y`, add new API version
- `0.y+1`, make new API version stored version and mark old API version as deprecated
- `0.y+2`, make `served=false` on old API version
- `0.y+3`, remove old API version

The reasoning is to give your end users some intermediate releases where both APIs are still present and gives some time for them to migrate to using the new version.

The general flow I shared above should generally fall under the same rough release cycle Kubernetes uses for deprecation and removal of beta API versions.

I think the most important thing here is to take your users into consideration. If your users assume that your API versions are pretty stable and are being used heavily, you may want to give them a longer migration cycle - but that is ultimately up to project maintainers to agree on.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T19:47:26Z

@everettraven thank you for the summary!

> In general, that looks something like:
> - `0.y`, add new API version
> - `0.y+1`, make new API version stored version and mark old API version as deprecated
> - `0.y+2`, make `served=false` on old API version
> - `0.y+3`, remove old API version

Let me map that onto the tentative plan I'm thinking about:
- `0.15.0`, new v1beta2 released, we deprecated v1beta1 in patch release; v1beta1 used for storage
- `0.16.0` end of Jan (next week), v1beta1 depreacted, v1beta2 for storage
- `0.17.0` end of march, we will continue: v1beta1 depreacted, v1beta2 for storage
- `0.18.0` end of may, make `served=false` on v1beta1
- `0.19.0` end of july, remove old v1beta1

So our current plan is even more relaxed, as we plan 0.17.0 to continue as 0.16.0 wrt to API versions support.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-23T05:28:00Z

> [@everettraven](https://github.com/everettraven) thank you for the summary!
> 
> > In general, that looks something like:
> > 
> > * `0.y`, add new API version
> > * `0.y+1`, make new API version stored version and mark old API version as deprecated
> > * `0.y+2`, make `served=false` on old API version
> > * `0.y+3`, remove old API version
> 
> Let me map that onto the tentative plan I'm thinking about:
> 
> * `0.15.0`, new v1beta2 released, we deprecated v1beta1 in patch release; v1beta1 used for storage
> * `0.16.0` end of Jan (next week), v1beta1 depreacted, v1beta2 for storage
> * `0.17.0` end of march, we will continue: v1beta1 depreacted, v1beta2 for storage
> * `0.18.0` end of may, make `served=false` on v1beta1
> * `0.19.0` end of july, remove old v1beta1
> 
> So our current plan is even more relaxed, as we plan 0.17.0 to continue as 0.16.0 wrt to API versions support.

Thank you! Updated https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3729056171.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:07:53Z

> "Kueue plans to make `v1beta2` the primary storage version in v0.16. "

This is not a plan, this is already committed.

> Support for `v1beta1` will end in later releases: `served=false` in v0.18

This is a plan, let's emphasize that.

I will slight tweak the wording here to make it closer to the suggestion in https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3767678919. Again, I don't think we should be committing to specific versions now.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:13:12Z

### Migrating Kueue Resources to API Version `v1beta2`

Kueue v0.16 starts using `v1beta2` API version for storage. Consequently, all new Kueue objects created after the upgrade will be stored using `v1beta2`. 

However, existing objects are only auto-converted to the new storage version by Kubernetes during a write request. This means that Kueue API objects that rarely receive updates - such as Topologies, ResourceFlavors, or long-running Workloads - may remain in the older `v1beta1` format indefinitely.

Ensuring all objects are migrated to `v1beta2` is essential for compatibility with future Kueue upgrades. We tentatively plan to discontinue support for `v1beta1` in version 0.18.

To ensure your environment is consistent, we recommend running the following migration script after installing Kueue v0.16 and verifying cluster stability. The script triggers a "no-op" update for all existing Kueue objects, forcing the API server to pass them through conversion webhooks and save them in the `v1beta2` version.

#### Steps

1. Download the official migration script:

   ```bash
   curl -O https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh
   chmod +x migrate-to-v1beta2.sh
   ```

2. Execute the script:

   ```bash
   ./migrate-to-v1beta2.sh
   ```

   - The script automatically detects and migrates all relevant Kueue resources (namespaced and cluster-scoped).
   - It requires `kubectl` access with permissions to patch Kueue CRs.
   - Progress and completion are displayed in the output.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:14:48Z

Posted the proposal in https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3788710736, but let me also hear from @tenzen-y and @gabesaba.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:16:16Z

/close 
Let me close to emphasize the implementaiton work is done. We can continue the discsussion on wording the release notes after the issue is closed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-23T07:16:23Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8018#issuecomment-3788719350):

>/close 
>Let me close to emphasize the implementaiton work is done. We can continue the discsussion on wording the release notes after the issue is closed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
