# Issue #8873: VisibilityOnDemand: inaccurate OpenAPI schema

**Summary**: VisibilityOnDemand: inaccurate OpenAPI schema

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8873

**Last updated**: 2026-02-11T07:54:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-29T16:55:22Z
- **Updated**: 2026-02-11T07:54:36Z
- **Closed**: 2026-01-30T09:41:46Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When I upgrade Kueue version from v0.15.3 to v0.16.0, I faced the following errors in ArgoCD:

```shell
failed to load open api schema while syncing cluster cache: error getting openapi resources: SchemaError(sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadsSummary.items): unknown model in reference: "sigs.k8s.io~1kueue~1apis~1visibility~1v1beta1.PendingWorkload"
```

As a result, ArgoCD doesn't work well across all Argo Applications since ArgoCD keeps failing to construct the cluster cache inside ArgoCD.

**What you expected to happen**:
No scheme errors.

**How to reproduce it (as minimally and precisely as possible)**:
To reproduce this problem, we need to set up [ArgoCD](https://github.com/argoproj/argo-cd) and manage Kueue as an ArgoApplication.

**Anything else we need to know?**:
After I removed all APIServices (`v1beta1.visibility.kueue.x-k8s.io` and `v1beta2.visibility.kueue.x-k8s.io`) for the visibility servers, this error has gone away. 
If either removing only the v1beta1 APIService or only the v1beta2 APIService, the described error isn't resolved.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.34.2
- Kueue version (use `git describe --tags --dirty --always`): v0.16.0
- Cloud provider or hardware configuration: Baremetal
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-29T16:57:31Z

This is possibly a sibling issue with our observation: https://github.com/kubernetes-sigs/kueue/issues/8780
So, I am doubting that Kueue VisibilityOnDemand has some issues instead of the ArgoCD issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T17:00:21Z

cc @vladikkuzn @mbobrovskyi who also observed the issue

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T17:01:00Z

I think this is high priority, because it errors if users will want to upgrade 0.16.0 -> 0.16.1, for example

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T17:01:09Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-29T17:04:21Z

For anyone who faces this issue, the mitigation way is only disabling the VisibilityOnDemand feature, but if you deeply depend on the feature, the only way to resolve this is to roll back to v0.15.3 😓 

> After I removed all APIServices (v1beta1.visibility.kueue.x-k8s.io and v1beta2.visibility.kueue.x-k8s.io) for the visibility servers, this error has gone away.
If either removing only the v1beta1 APIService or only the v1beta2 APIService, the described error isn't resolved.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-29T17:06:08Z

/assign @vladikkuzn 

Who is working on this issue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-29T17:09:44Z

Yes, this was introduced in this PR: https://github.com/kubernetes-sigs/kueue/pull/8312. The problem is that our Visibility OpenAPI was generated incorrectly: https://github.com/kubernetes-sigs/kueue/blob/92b06c598bd2f6775cec0a1c77e05d0ef3dbbe21/apis/visibility/openapi/zz_generated.openapi.go#L88-L101. We need to migrate this somehow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-29T17:12:58Z

> Yes, this was introduced in this PR: [#8312](https://github.com/kubernetes-sigs/kueue/pull/8312). The problem is that our Visibility OpenAPI was generated incorrectly:
> 
> [kueue/apis/visibility/openapi/zz_generated.openapi.go](https://github.com/kubernetes-sigs/kueue/blob/92b06c598bd2f6775cec0a1c77e05d0ef3dbbe21/apis/visibility/openapi/zz_generated.openapi.go#L88-L101)
> 
> Lines 88 to 101 in [92b06c5](/kubernetes-sigs/kueue/commit/92b06c598bd2f6775cec0a1c77e05d0ef3dbbe21)
> 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.ClusterQueue":            schema_kueue_apis_visibility_v1beta1_ClusterQueue(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.ClusterQueueList":        schema_kueue_apis_visibility_v1beta1_ClusterQueueList(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.LocalQueue":              schema_kueue_apis_visibility_v1beta1_LocalQueue(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.LocalQueueList":          schema_kueue_apis_visibility_v1beta1_LocalQueueList(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkload":         schema_kueue_apis_visibility_v1beta1_PendingWorkload(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadOptions":  schema_kueue_apis_visibility_v1beta1_PendingWorkloadOptions(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadsSummary": schema_kueue_apis_visibility_v1beta1_PendingWorkloadsSummary(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.ClusterQueue":            schema_kueue_apis_visibility_v1beta2_ClusterQueue(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.ClusterQueueList":        schema_kueue_apis_visibility_v1beta2_ClusterQueueList(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.LocalQueue":              schema_kueue_apis_visibility_v1beta2_LocalQueue(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.LocalQueueList":          schema_kueue_apis_visibility_v1beta2_LocalQueueList(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.PendingWorkload":         schema_kueue_apis_visibility_v1beta2_PendingWorkload(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.PendingWorkloadOptions":  schema_kueue_apis_visibility_v1beta2_PendingWorkloadOptions(ref), 
>  "sigs.k8s.io/kueue/apis/visibility/v1beta2.PendingWorkloadsSummary": schema_kueue_apis_visibility_v1beta2_PendingWorkloadsSummary(ref), 
> . We need to migrate this somehow.

Thank you for pointing that out. Yea, the problem introduction PR (#8312) matches with my investigations.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-29T20:38:24Z

Yeah, I'm looking for an option to generate it automatically

### Comment by [@25laker](https://github.com/25laker) — 2026-01-29T22:05:44Z

Thanks for reporting this! One thing I’ve noticed in projects using OpenAPI is that schema inconsistencies sometimes lead to unexpected behavior or even security gaps, especially when access patterns or data flows aren’t fully validated. Performing a semantic review of the API’s intended behavior before deployment can help catch these mismatches early and reduce potential risks. Curious if others have tried similar approaches?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-10T15:31:36Z

Hello,

In openshift we are still getting this problem on main. https://github.com/openshift/kueue-operator/pull/1369

The e2e test that was added is failing and I'm not entirely sure the resolution.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T07:54:36Z

> Hello,
> 
> In openshift we are still getting this problem on main. [openshift/kueue-operator#1369](https://github.com/openshift/kueue-operator/pull/1369)
> 
> The e2e test that was added is failing and I'm not entirely sure the resolution.

@kannon92 I pinned the solution to this issue. After you upgrade the Kueue version to v0.16.1, this should be resolved, btw.
