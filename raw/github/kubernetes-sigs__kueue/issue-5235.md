# Issue #5235: Kueue controller is trying to access third party GVKs which doesn't have access to

**Summary**: Kueue controller is trying to access third party GVKs which doesn't have access to

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5235

**Last updated**: 2025-05-15T17:37:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@pierDipi](https://github.com/pierDipi)
- **Created**: 2025-05-12T16:50:19Z
- **Updated**: 2025-05-15T17:37:15Z
- **Closed**: 2025-05-15T17:37:15Z
- **Labels**: `kind/bug`, `kind/regression`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 15

## Description

**What happened**:

I'm trying to use Kueue with Kserve for model inference (through the Deployment and Pod integration) and I'm seeing many error logs in the Kueue controller manager like:

```
W0512 16:37:49.006396       1 reflector.go:569] sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: failed to list *v1.PartialObjectMetadata: inferenceservices.serving.kserve.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "inferenceservices" in API group "serving.kserve.io" at the cluster scope
E0512 16:37:49.006442       1 reflector.go:166] "Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: inferenceservices.serving.kserve.io is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"inferenceservices\" in API group \"serving.kserve.io\" at the cluster scope" logger="UnhandledError"
```

**What you expected to happen**:

No error logs.

**How to reproduce it (as minimally and precisely as possible)**:

1. Clone this repo https://github.com/pierDipi/kueue-access-unknown-gvks
    `git clone git@github.com:pierDipi/kueue-access-unknown-gvks.git`
1. Run `kind create cluster`
2. Run `./repro.sh`
3. See error logs: `kubectl logs -n kueue-system -l=control-plane=controller-manager -f`

**Anything else we need to know?**: I don't want to give Kueue access to a resource that doesn't need to have access to.

**Environment**: KinD
- Kubernetes version (use `kubectl version`): 
  ```
  $ kubectl version
  # ...
  Server Version: v1.32.2
  ```
- Kueue version (use `git describe --tags --dirty --always`): 0.11.4 (latest as of today)
- Cloud provider or hardware configuration: N/A
- OS (e.g: `cat /etc/os-release`): Linux (Fedora)
- Kernel (e.g. `uname -a`): N/A

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T18:00:32Z

This is probably related to the recent updates in [FindAncestorJobManagedByKueue](https://github.com/kubernetes-sigs/kueue/blob/0db959e83edda267222125cbca98ab1f41c796ac/pkg/controller/jobframework/reconciler.go#L691). 

The intention was two be able to support AppWrapper and be able to traverse the ownership chain without requiring management of the CRDs on the way. 

I'm wondering if we could patch this just by checking in advance if Kueue has the required access to read the CRD. If it does not have, then it will not work anyway.

cc @dgrove-oss  @tenzen-y @mbobrovskyi

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-12T18:49:02Z

We probably should patch it by catching the error, realizing we don't have read access, logging it at the debug level, and not returning an error to the controller runtime.

It's not directly relevant, but I did notice that in the [provided reproducer yaml,](https://github.com/pierDipi/kueue-access-unknown-gvks/blob/9626645572a7990b12f771d00f61955ea1422027/500-isvc.yaml#L6-#L20) the `InferenceService` has a queue-name label.  If Kueue isn't allowed to read InferenceService, that label is not going to be useful.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T18:55:48Z

> We probably should patch it by catching the error, realizing we don't have read access, logging it at the debug level, and not returning an error to the controller runtime.

right this would work but realizing we don't have read access may require parsing the error which isn't clean, it might be a necessity. Im wondering if there is some API/function which would allow to check us if we have the read access prior to the attempt of reading.

### Comment by [@pierDipi](https://github.com/pierDipi) — 2025-05-13T07:08:57Z

> It's not directly relevant, but I did notice that in the [provided reproducer yaml,](https://github.com/pierDipi/kueue-access-unknown-gvks/blob/9626645572a7990b12f771d00f61955ea1422027/500-isvc.yaml#L6-#L20) the `InferenceService` has a queue-name label. If Kueue isn't allowed to read InferenceService, that label is not going to be useful.

As a note, the label is at the InferenceService level because we leverage Kserve labels propagation to propagete the Queue label to the Deployment/Pods.

### Comment by [@pierDipi](https://github.com/pierDipi) — 2025-05-13T07:12:10Z

> Im wondering if there is some API/function which would allow to check us if we have the read access prior to the attempt of reading

We can use `SelfSubjectAccessReview` API with get, list, watch verbs?
- https://kubernetes.io/docs/reference/access-authn-authz/authorization/#checking-api-access
- https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/self-subject-access-review-v1/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T07:30:17Z

Looks promising, we would need to check how this can be used by a go-client in Kueue code.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-13T23:42:34Z

I think this is another example of this error manifesting itself:

https://github.com/kubernetes-sigs/kueue/issues/4141#issuecomment-2877537125

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T12:42:29Z

/assign 
Tentatively, as this is an important regression. 

However, I'm loaded with other release-related tasks, so if there is someone who is willing to look into this, then be my guest :)

### Comment by [@qti-haeyoon](https://github.com/qti-haeyoon) — 2025-05-15T04:16:52Z

Regardless of the planned patch (which is to check access before attempting to read), should users update the Kueue controller's [ClusterRole](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/rbac/role.yaml) manifest if we use third party GVK?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T06:50:49Z

/kind regression
Since this was not an issue prior to 0.11.4.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T07:00:26Z

> Regardless of the planned patch (which is to check access before attempting to read), should users update the Kueue controller's [ClusterRole](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/rbac/role.yaml) manifest if we use third party GVK?

This is a good question. The answer will depend on the way we decide to fix it, but I would strive to preserve the previous behavior (before 0.11.4), so this is not needed. 

I believe the problematic PR is this: https://github.com/kubernetes-sigs/kueue/pull/4824, which tries to walk up the owner reference even outside of frameworks recognized by Kueue. This may be a nice feature, but I don't think this was required as a bugfix. This PR aimed to support AppWrapper properly it seems in cases where the interim framework is either custom or known but disabled.

However, the problem with that is we may walk into frameworks we don't have permission for. And checking permission is hard. Yes, we have `SelfSubjectAccessReview`, but this is actually a wrapper around a POST call to the API-server. I don't think we can afford sending these posts from our webhooks (and the traversal function is used in webhooks). Similarly, I don't think even capturing the error as suggested in https://github.com/kubernetes-sigs/kueue/issues/5235#issuecomment-2873659015 would not be feasible, because it means that controller-runtime repeatedly will send requests to API server to LIST the resource and fail, this seems like too much churn.

So, the way I would propose to fix the regression, and yet maintain the fix  https://github.com/kubernetes-sigs/kueue/pull/4824 would be to only walk up the ownership over known frameworks (enabled + disabled + listed in externalFrameworks). This way we make sure, that if an admin wants some custom framework to work with AppWrapper they can list it inside externalFrameworks. And to be fair, it is probably ok to only walk over enabled + externalFrameworks. Then users of AppWrapper who want to use it for disabled built-in integrations could add the integration into the list of externalFrameworks.

If this approach gets support it will not require changes to the permissions.

cc @tenzen-y @dgrove-oss @PBundyra @gabesaba let me know if you have some opinions.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T08:41:05Z

> And to be fair, it is probably ok to only walk over enabled + externalFrameworks. Then users of AppWrapper who want to use it for disabled built-in integrations could add the integration into the list of externalFrameworks.

Does this mean the following framework enabling and disabling?

```yaml
integration:
  frameworks:
  - "batch/job"
  - "workload.codeflare.dev/appwrapper"
  externalFrameworks:
  - "jobset.x-k8s.io/jobset"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T09:03:38Z

Yes, but I'm hesitant between two options, you posted like in (1.):

1. 
- only consider looking up for workload for enabled integrations + externalFrameworks
- walk up ownership only for enabled integrations + externalFrameworks (stop on disabled integrations)

2. 
- only consider looking up for workload for enabled integrations + externalFrameworks
- walk up ownership only for enabled and disabled built-in integrations + externalFrameworks

I think actually (2.) might be less work, and less breaking to admins. It should be ok, because for the disabled integrations we provide RBAC permissions with Kueue, so we can walk up.  This would be minimal fix to only exclude walking up the tree for unknown frameworks completely. 

So, I'm now leaning to (2). wdyt? 

EDIT: in other words, externalFrameworks would only be needed for CustomJobs wrapped by AppWrapper. Not for JobSet as Kueue knows it provides RBAC for JobSet.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-15T13:01:16Z

My recollection of the situation we were trying to fix by doing this is that we have to walk through disabled integrations (eg, suppose Job integration is disabled, but JobSet is enabled).  But option 2 should work.... we look through any kind that Kueue is capable of managing (enabled or disabled), but stop when we find something we don't know about.  And it is simpler since we don't have to do a potentially complex subject access review.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:30:16Z

> I think actually (2.) might be less work, and less breaking to admins. It should be ok, because for the disabled integrations we provide RBAC permissions with Kueue, so we can walk up. This would be minimal fix to only exclude walking up the tree for unknown frameworks completely.
> 
> So, I'm now leaning to (2). wdyt?

I'm fine with (2). Today, we have StatefulSet and Deployment supports. The popular OSS projects often depend on those core resources, like Knative. I think (2) would work well.
