# Issue #867: Is it possible to support queueing deployment?

**Summary**: Is it possible to support queueing deployment?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/867

**Last updated**: 2025-06-10T14:59:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lizzzcai](https://github.com/lizzzcai)
- **Created**: 2023-06-19T07:52:32Z
- **Updated**: 2025-06-10T14:59:52Z
- **Closed**: 2025-06-10T14:59:51Z
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->

Hi experts,

I found this project and am keen on exploring it on queueing the job (for example argo workflow). I am wondering if k8s deployment is supported as well? or is it possible to extend it to support queueing deployment (as I saw [custom workload](https://kueue.sigs.k8s.io/docs/concepts/workload/#custom-workloads) in the doc). If yes, is there any doc and how easy it is to support a custom workload. 

The reason I checked with deployment is that I like the feature (resource quota and the good local queue isolation) supported in this project and I am thinking if it is capable to be a generic quota management service to all the workload (not just job, but pod as well.)

Thanks.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-19T12:34:19Z

It is currently not in our roadmap, as Deployments don't have the concept of completion.

But yes, you could implement an integration controller to support deployments. Here is the framework to implement these controllers https://github.com/kubernetes-sigs/kueue/tree/main/pkg/controller/jobframework. We haven't had the chance to write a tutorial about this yet. Also the framework is still evolving, as we integrate more CRDs.

The key concept you have to implement is the idea of "suspend": when a job is suspended, there shouldn't be any pods. I think you could implement this in the deployment by setting the replicas to zero and storing the target number of replicas in some annotation.

You can also integrate Pods. The suspend concept can be implemented using [Scheduling gates](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/). But pods cannot be restarted, so once preempted the pod is failed and you have to re-submit.

### Comment by [@lizzzcai](https://github.com/lizzzcai) — 2023-06-19T15:52:31Z

Hi @alculquicondor , thanks for your reply and explanation, I will look into it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-31T15:01:14Z

Hello @lizzzcai, if you looked into this, would you be interested in contributing the controller, as part of #1088 ?

### Comment by [@lizzzcai](https://github.com/lizzzcai) — 2023-09-13T06:10:17Z

> Hello @lizzzcai, if you looked into this, would you be interested in contributing the controller, as part of #1088 ?

Hi @alculquicondor, sorry for the late reply. I probably can look into it in my free time but I can not provide a timeline here.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-28T06:59:48Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-27T07:48:27Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-27T13:28:51Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:00:06Z

/remove-kind support
/kind feature

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-10T14:59:46Z

Kueue supports deployment now so we can close this.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-10T14:59:52Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/867#issuecomment-2959597270):

>Kueue supports deployment now so we can close this.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
