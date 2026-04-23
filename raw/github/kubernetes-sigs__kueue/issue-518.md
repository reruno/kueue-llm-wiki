# Issue #518: Record injected node affinity in batch Job

**Summary**: Record injected node affinity in batch Job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/518

**Last updated**: 2023-08-18T13:14:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-01-16T10:50:27Z
- **Updated**: 2023-08-18T13:14:30Z
- **Closed**: 2023-08-18T13:14:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 39

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When we want to suspend Job, we'd like to restore the original nodeAffinity, but some times we can't find the derived workload, see https://github.com/kubernetes-sigs/kueue/blob/045697c46f307b37a03f57f3b42d11a74fe01927/pkg/controller/workload/job/job_controller.go#L397-L402

I'd like to add the nodeAffinity to Job annotations to make this an accurate one. It would like:
```
annotations: kueue.sig.kubernetes.io/injected-node-affinity: '{"key1": "value1", "key2": "value2"}'
```

**Why is this needed**:

Always make sure that when suspending a Job, we'll restore the original nodeAffinity.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-16T10:53:03Z

cc @ahg-g as the first author.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-16T19:24:03Z

My concern is that this will add another update request for every job. Is this cost justified?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-01T21:55:31Z

It can be the same API call that updates the Job spec.

However, maybe we should store the original node selector instead of the injected one.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-02-28T00:18:44Z

Note that when the job is suspended, the controller will reset the nodeSelector on the job: https://github.com/kubernetes-sigs/kueue/blob/b2a5e386d7e9c0e3346660dd01001734f631d7fd/pkg/controller/workload/job/job_controller.go#L352

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-28T03:09:01Z

> Note that when the job is suspended, the controller will reset the nodeSelector on the job:

Yes, but sometimes the corner case could be job is unsuspended, but the workload is deleted in an unknown condition, like delete in manual, then the job will maintain a wrongly configured nodeSelector.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-03-06T15:15:56Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-03-06T15:49:53Z

> > Note that when the job is suspended, the controller will reset the nodeSelector on the job:
> 
> Yes, but sometimes the corner case could be job is unsuspended, but the workload is deleted in an unknown condition, like delete in manual, then the job will maintain a wrongly configured nodeSelector.

Right, it is ok to record the original nodeSelector as long as it is done in the same nodeSelector update request, but I think it is worth having a discussion on whether we want to attach the workload's life with the job using finalizers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-06T17:05:05Z

Deleting a Workload seems like  an important tool for forcing a requeue and adding finalizers could further complicate this use case.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-09T07:14:55Z

> whether we want to attach the workload's life with the job using finalizers

Add a finalizer to workload, when to delete the workload, restore the node selector with Job. Seems more convincible. I prefer to not use annotation if we can. But yes, we will have to handle the terminating workload in job reconciling.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-22T14:43:04Z

it's `/assign`

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-22T14:44:16Z

@mimowo could you take on a review for a future PR on this, in the context of the job integration framework?

### Comment by [@trasc](https://github.com/trasc) — 2023-03-22T14:44:49Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-03-22T15:03:04Z

> @mimowo could you take on a review for a future PR on this, in the context of the job integration framework?

Sure.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-31T20:32:04Z

I'm now wondering whether we should revert this, as we have a growing number of annotations to support partial admission.

On support of this feature, we have resiliency: we can loose the Workload object and we can still recover the job.

However, is it worth?

- End users can't modify workloads by default https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/workload_editor_role.yaml
- There are concerns about sizes of the Job manifests upstream https://github.com/kubernetes/kubernetes/issues/118085, then certainly adding a big annotation doesn't help.

cc @tenzen-y @trasc 

I think we can just document that users (including admins) shouldn't remove a Workload object.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-31T20:32:14Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-31T20:32:18Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/518#issuecomment-1570907786):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-01T09:50:36Z

> I think we can just document that users (including admins) shouldn't remove a Workload object

Or leveraging finalizers here, when deleting jobs, we'll restore the node affinity and then remove the finalizer.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T12:03:10Z

The finalizers alternative require careful thinking too. We don't want to accidentally leave objects with finalizers. The problem here is that the Job object is a parent of the Workload object. As such, the Job can't be deleted unless the Workload is deleted first. Then we have a circular dependency.

Another alternative is that a Workload has a finalizer if it's admitted. But the complication is that finalizers are not part of the status, so we need additional API calls.

Not sure if it's worth the effort, but worth exploring.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-01T14:00:40Z

RE: It's not delete the job but delete the workload. The problem we can't restore the node affinity is because workload might be deleted accidentally, now we add the finalized to the workload, when we want to delete the workload, we'll restore the Job, then remove the finalizer, the workload will be deleted finally.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-01T17:24:47Z

> I'm now wondering whether we should revert this, as we have a growing number of annotations to support partial admission.

Yea... Our annotations are so big...

> It's not delete the job but delete the workload. The problem we can't restore the node affinity is because workload might be deleted accidentally, now we add the finalized to the workload, when we want to delete the workload, we'll restore the Job, then remove the finalizer, the workload will be deleted finally.

That probably works fine. But we need to evaluate whether it is worth doing even if making more API calls as @alculquicondor says.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T09:16:33Z

An alternative could be to have an additional custom resource just to back-up selectors and counts. This resource should be owned by the job, so after we are creating / update it before unsuspending the job, we do not need to keep track of it's lifecycle. 

We will have additional API calls, but they should not trigger any  controller.
  
@alculquicondor @kerthcet @tenzen-y  WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T15:13:11Z

Another CRD would have the same issue about needing a finalizer.

The workload is already an object that end-users shouldn't have permissions to edit or delete.

I prefer we get rid of the annotation, without any finalizer in the Workload. And re-evaluate in the future if we find a use case where end-users need to modify the Workload object.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T17:37:05Z

> Another CRD would have the same issue about needing a finalizer.

Not exactly, there is no delete conditioning ,  when the job gets deleted so it's the "backup" resource.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T17:44:20Z

The Job also owns the Workload. So when we delete the Job, the Workload gets deleted as well.

The problem is what happens if someone (not Kueue) deletes the Workload prematurely.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T17:47:33Z

Yes the problem is when the workload gets deleted before the restore, in that  case the backup resource will still exists, and the restore can be done from that. 

When the job gets deleted ... we don't actually care what is happening to the selectors and counts.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T17:49:43Z

But what's the difference between the "backup" resource and Workload? They are both subject to an unauthorized deletion. I don't see any difference, so I rather have one object.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-06T18:01:41Z

The key here is that end-users accidentally remove resources storing original job information. 
So, I think the problem isn't solved even if we introduce another CRD.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T19:09:24Z

I don't see accidental removal as a real problem, the chances of it to happen is the same as accidental removal of the job, however with a different  resource a queue administrator could make sure that "end-users accidentally remove resources storing original job information" by RBAC.

During the review of the original implementation, I think, workload deletions was presented as a valid way to requeue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T19:30:39Z

Right... that's an easy way of evicting a workload and put it in the front of the queue.

The alternative would be that the administrator only deletes the `admission` field in the status, but this puts the job in the back of the queue.

A finalizer would still be a more perfomant solution than having a second object. The question would be which controller removes the finalizer?
~I guess it could be the workload controller itself, based on whether the Admitted=true condition is present.~
It has to be each job controller, based on whether the original spec was restored after the Workload has a deletionTimestamp.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T19:34:12Z

I would suggest we mark the deletion of a Workload as "unsupported behavior" to start.

@tenzen-y @kerthcet are you ok with that?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-06T20:05:42Z

> I would suggest we mark the deletion of a Workload as "unsupported behavior" to start.

Does that mean we say the note in the document?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T20:19:46Z

yes

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-06T20:28:46Z

Agree.

Additionally, we might want to consider another way to re-enqueue the job.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-07T04:07:22Z

SGTM, the ROI is high 😄

### Comment by [@mimowo](https://github.com/mimowo) — 2023-06-07T07:22:11Z

Does it make sense to consider a knob in Kueue configuration whether to store the annotation?

Some users wouldn't be concerned about Job size (reasons may vary: 1. using non-indexed jobs, 2. using small node selectors, or using indexed jobs with small parameters), but may be concerned about losing track of node selectors.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-07T11:22:56Z

I think the motivation here is avoid to use too many annotations from the POV of kueue. If we have the ambition to push this to the upstream, it will be a stumbling stock. 🥲

### Comment by [@trasc](https://github.com/trasc) — 2023-06-07T12:35:33Z

I've opened a new PR for this #834, It's still in draft since is developed on top of #771.

More interesting for this discussion are:

- [commit no 1](https://github.com/kubernetes-sigs/kueue/pull/834/commits/7f7864f5194645d7a87b6e55d81667c5ba9d025a) which removes the use the annotations, but we should not delete workloads anymore
- [commit no 2](https://github.com/kubernetes-sigs/kueue/pull/834/commits/5819d7767f7ac9b00f1a850fe2fea92f6b0a50e3) adds and manages a finalizer in the workloads (this is still wip , need some cleanup and tests, but is functional)

Please have a look and let me know what you think.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-07T12:39:30Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-07T15:34:23Z

> Does it make sense to consider a knob in Kueue configuration whether to store the annotation?

I prefer we don't maintain such piece of code. We are also risking that the annotation changes name/contents from one version to the next, as we do more mutations during admission.
