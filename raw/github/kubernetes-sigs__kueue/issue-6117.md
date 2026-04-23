# Issue #6117: Make MultiKueue Admission Check Controller Reusable by External Frameworks

**Summary**: Make MultiKueue Admission Check Controller Reusable by External Frameworks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6117

**Last updated**: 2026-04-18T09:13:56Z

---

## Metadata

- **State**: open
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-07-21T13:04:39Z
- **Updated**: 2026-04-18T09:13:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 17

## Description

# Make MultiKueue Admission Check Controller Reusable by External Frameworks

**What would you like to be added**:

Enable external frameworks to run their own multikueue admission check controllers by making the multikueue implementation in Kueue reusable and configurable, similar to how the job framework pattern allows external frameworks to integrate with Kueue.

The proposed enhancement includes:

1. **Configurable Controller Name**: Make the hardcoded `MultiKueueControllerName` (`"kueue.x-k8s.io/multikueue"`) configurable in the multikueue admission check controller, allowing external frameworks to use their own controller names.

2. **Reusable MultiKueue Package**: Expose the multikueue implementation as a reusable library that external frameworks can import and configure with their own parameters.

3. **Enhanced Setup Options**: Extend the `SetupControllers` function to accept additional configuration options, including:
   - Custom controller name for admission check filtering
   - Framework-specific origin labels

4. **Framework Integration Pattern**: Provide a clear pattern for external frameworks to integrate multikueue functionality, similar to the existing job framework integration pattern.

**Why is this needed**:

Currently, the multikueue admission check controller is hardcoded to only handle admission checks with the controller name `"kueue.x-k8s.io/multikueue"`. This prevents external frameworks from reusing the valuable multikueue functionality for their own workloads.

**Current Limitation**: 
In `/pkg/controller/admissionchecks/multikueue/admissioncheck.go:65`, the controller has a hardcoded check:
```go
if err := a.client.Get(ctx, req.NamespacedName, ac); err != nil || ac.Spec.ControllerName != kueue.MultiKueueControllerName {
    return reconcile.Result{}, client.IgnoreNotFound(err)
}
```

This prevents external frameworks from creating their own multikueue-based admission checks by
reusing the code from the Kueue repository.

**Use Cases**:

**Third-party Integrations**: External job orchestration frameworks (like Tekton, Argo Workflows, Jenkins X, etc.) want to provide multikueue capabilities to their users.

**Benefits**:

1. **Reusability**: External frameworks can reuse Kueue's proven multikueue implementation without reimplementing the complex cross-cluster coordination logic.

2. **Consistency**: All frameworks benefit from the same battle-tested multikueue code, ensuring consistent behavior across different workload types.

3. **Maintenance**: Bug fixes and improvements in the core multikueue implementation automatically benefit all frameworks using it.

4. **Innovation**: External frameworks can focus on their domain-specific features while leveraging Kueue's multikueue capabilities.

## Discussion

### Comment by [@khrm](https://github.com/khrm) — 2025-07-21T16:03:55Z

In external jobframework approach, there's no communication between external controller and kueue. Both work independently.  But if we go with this idea, we need a way to communicate with our workload. We need a way to convey what to copy from manager to worker and back. Unless, you want to implement that also. If so, then you are just recreating the whole MultiKueue ACC.

Is my understanding correct or am I missing something?

### Comment by [@khrm](https://github.com/khrm) — 2025-07-21T16:05:06Z

Or do you want to be able to just copy workload, but offloading the syncing of  jobs to other controllers? That's another way.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-07-21T18:09:04Z

> In external jobframework approach, there's no communication between external controller and kueue. Both work independently. But if we go with this idea, we need a way to communicate with our workload. 

what do you mean commuincate with a workload? a workload is reconciled by the ACC. 

> We need a way to convey what to copy from manager to worker and back. Unless, you want to implement that also. If so, then you are just recreating the whole MultiKueue ACC.

When you are saying recreated what do you mean?
I'm asking because what I suggest can be seen as replicating the MultiKueue ACC, but I also suggest to make its code available to other to import, so there is not code duplication.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T18:31:59Z

Ideally, I would like to have a design where the AC is decoupled from Job createtion and syncing. So there is only one MultiKueue admission check, and it orchestrates the prebuilt workloads. Once a prebuilt workload is admitted to one of the worker clusters then a external controller would create the actual Job copy and will sync its status.

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-08-09T19:33:23Z

> Ideally, I would like to have a design where the AC is decoupled from Job createtion and syncing. So there is only one MultiKueue admission check, and it orchestrates the prebuilt workloads. Once a prebuilt workload is admitted to one of the worker clusters then a external controller would create the actual Job copy and will sync its status.

This architecture might also help external controllers to use the cluster chosen by multi-kueue admission and sync the workloads there. I believe that is what you are alluding to as well

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T06:59:12Z

> > Ideally, I would like to have a design where the AC is decoupled from Job createtion and syncing. So there is only one MultiKueue admission check, and it orchestrates the prebuilt workloads. Once a prebuilt workload is admitted to one of the worker clusters then a external controller would create the actual Job copy and will sync its status.
> 
> This architecture might also help external controllers to use the cluster chosen by multi-kueue admission and sync the workloads there. I believe that is what you are alluding to as well

Yes, the idea was that the MultiKueue AC creates the prebuilt-workloads and does dispatching. Once the cluster is selected (now status.clusterName), then the external controller supplied by the user would sync it. I think avoiding maintaining a separate external AC for MultiKueue is a big gain for users, for example to ease debugging.

Now, one complication I didn't foresee is that the external Job controller would still need to read and respect the secret, and so it would be reading Kueue configuration, which is extra dev cost for users. Thus, I like https://github.com/kubernetes-sigs/kueue/pull/5981, it enables MK support for simple jobs with just a couple of lines of ConfigMap yaml. We may still consider refactoring long term, but given the simplicity of the proposal, I'm good with it as the first step.

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-08-20T06:42:33Z

> I didn't foresee is that the external Job controller would still need to read and respect the secret, and so it would be reading Kueue configuration, which is extra dev cost for users. 

Just to be clear, I built a downstream controller which can create workload object in the manager cluster and then syncs the CR in the workload cluster, which I feel seems reasonable. I had to relax the restriction on admission controller to accept unknown CRDs, I was thinking of having a field in the externalFramework in kueue config(which says `disableSyncing: true` or vice-versa) and let the external controller handling it. Slowly, we can make this field default. This way multi-kueue just does the cluster selection and let the external entity(controller) deal with syncing. It can help moving the syncing from push based model to pull based if wanted at a later stage.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-08-20T07:34:21Z

> > I didn't foresee is that the external Job controller would still need to read and respect the secret, and so it would be reading Kueue configuration, which is extra dev cost for users.
> 
> Just to be clear, I built a downstream controller which can create workload object in the manager cluster and then syncs the CR in the workload cluster, which I feel seems reasonable. I had to relax the restriction on admission controller to accept unknown CRDs, I was thinking of having a field in the externalFramework in kueue config(which says `disableSyncing: true` or vice-versa) and let the external controller handling it. Slowly, we can make this field default. This way multi-kueue just does the cluster selection and let the external entity(controller) deal with syncing. It can help moving the syncing from push based model to pull based if wanted at a later stage.

Did you reuse any of the multikueue code from this repo? If so how did you overcome the hard coded name of the admission check controller /pkg/controller/admissionchecks/multikueue/admissioncheck.go:65 ?

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-08-20T14:33:43Z

> Did you reuse any of the multikueue code from this repo? If so how did you overcome the hard coded name of the admission check controller /pkg/controller/admissionchecks/multikueue/admissioncheck.go:65 ?

Forked kueue and modified the admission controller. This is what I meant by:
```
I had to relax the restriction on admission controller to accept unknown CRDs, 
```

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-08-22T12:50:53Z

Related to https://github.com/kubernetes-sigs/kueue/pull/2458

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-08-27T05:03:48Z

Coming back to the discussion, how do you all feel about the MK having a  `disableSyncing: true ` field through which syncing can be disabled?

### Comment by [@wongma7](https://github.com/wongma7) — 2025-10-14T23:59:57Z

> Thus, I like https://github.com/kubernetes-sigs/kueue/pull/5981, it enables MK support for simple jobs with just a couple of lines of ConfigMap yaml. We may still consider refactoring long term, but given the simplicity of the proposal, I'm good with it as the first step.

Now that the generic adapter #5981 has merged, for next steps WDYT about extending its config to satisfy the use-case described here? Basically I would like to leverage the generic adapter for Workload copying & admission while delegating Job creation & syncing to my external controller.

The initial generic adapter doesn't work for my particular CRD because the CRD doesn't have spec.managedBy nor status subresource (and the CRD is basically impossible for me to change). So for the moment I am maintaining a fork of kueue with my own MultiKueueAdapter implementation. I think the gap could mostly be closed with two config options:

1. `disableSyncing` boolean (as proposed above) in MultiKueueExternalFramework https://github.com/kubernetes-sigs/kueue/blob/v0.14.1/apis/config/v1beta1/configuration_types.go#L291 so that `SyncJob/DeleteRemoteObject`MultiKueueAdapter responsibilities can be skipped & delegated to an external controller. In my case I would rather write & maintain an external controller with this set true than maintain a kueue fork, even if there is no library or support by kueue to help with the dev cost.
2. `managedByKueue` boolean in MultiKueueExternalFramework so that `IsJobManagedByKueue` can be determined in absence of a spec.managedBy field. In my case I am simply not going to run the CRD job controller in the manager cluster so I want to be able to default managed by kueue to `true` instead of throwing an error.

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-10-15T14:35:02Z

There was discussion around it on slack as well: https://kubernetes.slack.com/archives/C032ZE66A2X/p1757427606615429?thread_ts=1755181736.825669&cid=C032ZE66A2X

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T14:40:52Z

Yes, we are open to the follow up extending MK for external controllers. This requires a KEP update. I think one idea we discussed in the past was to introduce a new `controllerType: External` (assuming the current default would be `controllerType: Generic`), then it would assume "disable defaulting", and "not managed by kueue". 

cc @tenzen-y 

I would suggest extending this KEP https://github.com/kubernetes-sigs/kueue/pull/5981, along with the user-story and "design details".

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:25:38Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:54Z

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
