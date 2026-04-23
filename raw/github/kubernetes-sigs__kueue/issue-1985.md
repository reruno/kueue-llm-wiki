# Issue #1985: Support Volcano queue in Kueue

**Summary**: Support Volcano queue in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1985

**Last updated**: 2024-09-28T13:45:29Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@AllenXu93](https://github.com/AllenXu93)
- **Created**: 2024-04-16T05:39:17Z
- **Updated**: 2024-09-28T13:45:29Z
- **Closed**: 2024-09-28T13:45:28Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->
We have used volcano queue for quota schedule https://volcano.sh/en/docs/queue/ , but volcano is schedule for pod. We want to use kueue limit Pod's creating, to reduce APIServer's prestress.
Is there any way to use kueue and vocalno queue?

## Discussion

### Comment by [@googs1025](https://github.com/googs1025) — 2024-04-23T08:16:15Z

hi! Is there any more information you can provide? Does it mean that you want to use kueue queue to support the volcano scheduler?

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-23T12:00:06Z

> hi! Is there any more information you can provide? Does it mean that you want to use kueue queue to support the volcano scheduler?

Hi. We have already use volcano queue in our cluster,  we plan to use kueue for job's queue schedule. 
A simple way is to install kueue directly, but in cluster there are many CR about queue, like kuque's ClusterQueue LocalQueue, and volcano's queue. Any update to quota need to update both of them.
So I want to know, is there any plan to let kueue support other queue or quota configuration, like volcano queue or k8s's resourceQuota.
For example, Kueue's schedule and queue manager support queue's interface, we can add some plugin that provider other queue configuration source.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-04-24T04:01:55Z

We have the similar requirement, we use elastic quota in our environment and we need a controller to transfer between different quota systems. Maybe we can consider to create a controller and a framework to help create and control the quota systems. @alculquicondor HDYT? And I can help to build the controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T06:46:21Z

We had a similar discussion about ResourceQuota here: https://github.com/kubernetes-sigs/kueue/issues/696.
As a result, cluster admins should implement admission check controllers for the ResourceQuota by themselves. 
@AllenXu93 @KunWuLuan So, I guess that you can select the same approach for the volcano queue and ElasticQuota.

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-24T06:59:28Z

> We had a similar discussion about ResourceQuota here: #696. As a result, cluster admins should implement admission check controllers for the ResourceQuota by themselves. @AllenXu93 @KunWuLuan So, I guess that you can select the same approach for the volcano queue and ElasticQuota.

Thanks for your advice!
select admission check can help in volcano queue or ElasticQuota, but we still need to maintain multiple CR, for example I want to change the quota of queue cq-a, I need to modify both clusterQueue and volcano queue(or elasticQuota) CR. 
I don't know is there any plan to extend queue source, so that we can write queue plugin.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-04-24T07:00:51Z

@tenzen-y 
> As a result, cluster admins should implement admission check controllers for the ResourceQuota by themselves.

Thanks, I think maintaining two types of quota with the same semantics is a challenging task, so maybe admission check is not what I need.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T07:07:42Z

> > We had a similar discussion about ResourceQuota here: #696. As a result, cluster admins should implement admission check controllers for the ResourceQuota by themselves. @AllenXu93 @KunWuLuan So, I guess that you can select the same approach for the volcano queue and ElasticQuota.
> 
> Thanks for your advice! select admission check can help in volcano queue or ElasticQuota, but we still need to maintain multiple CR, for example I want to change the quota of queue cq-a, I need to modify both clusterQueue and volcano queue(or elasticQuota) CR. I don't know is there any plan to extend queue source, so that we can write queue plugin.

Yes, your understanding is correct. In that situation, we need to maintain multiple customresources to maintain quotas.
As we mentioned in the ResourceQuota discussion, ideal world, we should manage all quotas by kueue, and the admission check controllers for other quota management systems are interim approaches.
So, you could avoid double management after you remove dependencies for the volcano.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T07:09:23Z

> @tenzen-y
> 
> > As a result, cluster admins should implement admission check controllers for the ResourceQuota by themselves.
> 
> Thanks, I think maintaining two types of quota with the same semantics is a challenging task, so maybe admission check is not what I need.

As I mentioned above, the admission check controller for the other quota management systems is an interim approach.
So, we would recommend fully migrating to kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T14:50:26Z

> Maybe we can consider to create a controller and a framework to help create and control the quota systems. @alculquicondor HDYT? And I can help to build the controller.

It's something you can explore, but I wouldn't support having volcano APIs as dependencies of Kueue.

I have heard of people using kueue+volcano, but I think the approach they take is to leave quota management fully to Kueue, and use volcano only for the "gang-scheduling" capability.

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-25T11:56:38Z

> > Maybe we can consider to create a controller and a framework to help create and control the quota systems. @alculquicondor HDYT? And I can help to build the controller.
> 
> It's something you can explore, but I wouldn't support having volcano APIs as dependencies of Kueue.
> 
> I have heard of people using kueue+volcano, but I think the approach they take is to leave quota management fully to Kueue, and use volcano only for the "gang-scheduling" capability.

Yes, I prefer to use all in one queue quota like kueue's queue quota, pod schedule should not aware of quota. But the problem is kueue can't confirm admited job's pods scheduled (either volcano or default schedule) .

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T11:45:07Z

> > > Maybe we can consider to create a controller and a framework to help create and control the quota systems. @alculquicondor HDYT? And I can help to build the controller.
> > 
> > 
> > It's something you can explore, but I wouldn't support having volcano APIs as dependencies of Kueue.
> > I have heard of people using kueue+volcano, but I think the approach they take is to leave quota management fully to Kueue, and use volcano only for the "gang-scheduling" capability.
> 
> Yes, I prefer to use all in one queue quota like kueue's queue quota, pod schedule should not aware of quota. But the problem is kueue can't confirm admited job's pods scheduled (either volcano or default schedule) .

If we enable the waitForPodsReady, the kueue will re-queue the pending jobs. Please see docs for more details: https://kueue.sigs.k8s.io/docs/tasks/manage/setup_sequential_admission/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-30T12:44:10Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-29T13:01:37Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-28T13:45:23Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-28T13:45:28Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1985#issuecomment-2380645640):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
