# Issue #3943: Disabling VisibilityOnDemand feature gate blocks namespace deletion

**Summary**: Disabling VisibilityOnDemand feature gate blocks namespace deletion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3943

**Last updated**: 2025-01-13T09:52:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-01-08T17:04:47Z
- **Updated**: 2025-01-13T09:52:34Z
- **Closed**: 2025-01-13T09:52:34Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I installed Kueue with the VisbilityOnDemand feature disabled via ` --feature-gates=VisibilityOnDemand=false`.

I then created and attempted to delete a namespace.  The namespace deletion stalled indefinitely.

**What you expected to happen**:

I expected to be able to delete a namespace.

**How to reproduce it (as minimally and precisely as possible)**:

Deploy Kueue with  --feature-gates=VisibilityOnDemand=false.  I happened to install from master (bf4657adc) to verify
that #3908 didn't fix the problem, but I also saw the same incorrect behavior on Kueue 0.10 during the Christmas break.

`kubectl create ns test`

`kubectl delete ns test`

Namespace deletion will hang.

**Anything else we need to know?**:

Doing a get on the namespace gets:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  creationTimestamp: "2025-01-08T16:29:06Z"
  deletionTimestamp: "2025-01-08T16:29:15Z"
  labels:
    kubernetes.io/metadata.name: test
  name: test
  resourceVersion: "2497"
  uid: 461a7652-ae28-4029-acf9-104800161b17
spec:
  finalizers:
  - kubernetes
status:
  conditions:
  - lastTransitionTime: "2025-01-08T16:29:20Z"
    message: 'Discovery failed for some groups, 1 failing: unable to retrieve the
      complete list of server APIs: visibility.kueue.x-k8s.io/v1beta1: stale GroupVersion
      discovery: visibility.kueue.x-k8s.io/v1beta1'
    reason: DiscoveryFailed
    status: "True"
    type: NamespaceDeletionDiscoveryFailure
  - lastTransitionTime: "2025-01-08T16:29:20Z"
    message: All legacy kube types successfully parsed
    reason: ParsedGroupVersions
    status: "False"
    type: NamespaceDeletionGroupVersionParsingFailure
  - lastTransitionTime: "2025-01-08T16:29:20Z"
    message: All content successfully deleted, may be waiting on finalization
    reason: ContentDeleted
    status: "False"
    type: NamespaceDeletionContentFailure
  - lastTransitionTime: "2025-01-08T16:29:20Z"
    message: All content successfully removed
    reason: ContentRemoved
    status: "False"
    type: NamespaceContentRemaining
  - lastTransitionTime: "2025-01-08T16:29:20Z"
    message: All content-preserving finalizers finished
    reason: ContentHasNoFinalizers
    status: "False"
    type: NamespaceFinalizersRemaining
  phase: Terminating

```

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-08T17:05:04Z

/cc @varshaprasad96

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:38:20Z

I suspect that you installed the APIService resource (https://github.com/kubernetes-sigs/kueue/blob/main/config/components/visibility/apiservice_v1beta1.yaml). Could you check if your cluster has Kueue APIService resources. If your cluster has it, what if you remove that?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-08T20:44:35Z

Good guess :)

Yes, it installed:
```
(base) dgrove@Dave's IBM Mac kueue % kubectl get APIService 
NAME                                   SERVICE                                AVAILABLE                      AGE
...
v1beta1.visibility.kueue.x-k8s.io      kueue-system/kueue-visibility-server   False (FailedDiscoveryCheck)   3h11m
...
```

After I do `kubectl delete APIService v1beta1.visibility.kueue.x-k8s.io`, then namespace deletion works as expected.

I guess this is mainly a documentation issue then?   Disabling the feature requires more than just setting the feature flag to false.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:52:49Z

Thank you for checking that.

> I guess this is mainly a documentation issue then? Disabling the feature requires more than just setting the feature flag to false.

I think so, too. Would you mind opening PR to add notifications for APIService manifest in case of situations where they disable the VisibilityOndemand feature gate? I think we can add it to https://kueue.sigs.k8s.io/docs/tasks/manage/monitor_pending_workloads/pending_workloads_on_demand/.

After we remove the VisibilityOnDemand feature gate, we can remove the notification as well. We typically remove the GA feature gates after the GA feature has been two minor releases.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:53:21Z

/remove-kind bug
/kind support
