# Issue #3439: Raise an event when a WorkloadPriorityClass.kueue.x-k8s.io is not found

**Summary**: Raise an event when a WorkloadPriorityClass.kueue.x-k8s.io is not found

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3439

**Last updated**: 2025-08-28T01:26:03Z

---

## Metadata

- **State**: open
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2024-11-04T18:59:38Z
- **Updated**: 2025-08-28T01:26:03Z
- **Closed**: —
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@j4ckstraw](https://github.com/j4ckstraw)
- **Comments**: 22

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When a job is created with a specified  `kueue.x-k8s.io/priority-class` that does not exist ; then an event should be raised with a `Warning` level in the `namespace` of the `job` and with the job as the `involvedObject.name`

**Why is this needed**:
When such a job is created nothing happens and it is difficult for the user to understand what is wrong except by reading the kueue controller manager logs. As this may require admin privileges, user may just remain blocked while searching for information.

**Completion requirements**:

The keueue logs show the following error message:
```
{"level":"error","ts":"2024-11-04T18:56:42.686021656Z","caller":"controller/controller.go:329","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"low-priority-job-tg6tr","namespace":"keue-viz"},"namespace":"keue-viz","name":"low-priority-job-tg6tr","reconcileID":"1e033921-c262-401c-a462-28b74583ee51","error":"WorkloadPriorityClass.kueue.x-k8s.io \"low\" not found","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:227"}

```

The relevant part being:
```
error":"WorkloadPriorityClass.kueue.x-k8s.io \"low\" not found",
```

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T08:26:04Z

+1, 
I'm also wondering if we should consider deactivating such a workload as it will not get scheduled until some manual intervention. WDYT @tenzen-y ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T09:09:40Z

OTOH, maybe deactivating can be considered as a breaking change for some flows when the priority class is created after the workload or in parallel. So, I'm fine for just an event now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T09:24:54Z

> OTOH, maybe deactivating can be considered as a breaking change for some flows when the priority class is created after the workload or in parallel. So, I'm fine for just an event now.

I think that we should implement the validation webhook to verify if the specified PriorityClass exists in the cluster.
That is the same specifications as the core API PriorityClass.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T09:51:16Z

> I think that we should implement the validation webhook to verify if the specified PriorityClass exists in the cluster.

Technically we could but IIUC this means validation per Job CRD which is a lot of code.

> That is the same specifications as the core API PriorityClass.

I just tested it using batch/Job and referenced a non-existing `priorityClassName`, but the Pod creation failed (Kueue was not installed). Then an event is sent for the owner Job:
```
Warning  FailedCreate  4s (x5 over 19s)  job-controller  Error creating: pods "sample-job-a-qsvvf-" is forbidden: no PriorityClass with name non-existing was found
```
So, on vanilla k8s the Job creation isn't blocked, and we get an event on the Job object. I think reproducing this is reasonable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T09:54:31Z

> So, on vanilla k8s the Job creation isn't blocked, and we get an event on the Job object. I think reproducing this is reasonable.

Yeah, I indicated the Pod creation:

```shell
cat <<EOF | k apply -f -
> apiVersion: v1
kind: Pod
metadata:
  name: high-priority-pod
  namespace: default
spec:
  priorityClassName: high-priority
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
> EOF
Error from server (Forbidden): error when creating "STDIN": pods "high-priority-pod" is forbidden: no PriorityClass with name high-priority was found
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T10:00:30Z

I see, but IIUC `WorkloadPriorityClass` does not translate to Pods, so we wouldn't be able to capture that in pod webhook.

### Comment by [@akram](https://github.com/akram) — 2024-11-05T12:32:44Z

An additional 2cts: The admission controller should not protect from a later deletion of `WorkloadPriorityClass` .
One can create the workload with the existing `WorkloadPriorityClass` and then delete the `WorkloadPriorityClass` impacting already existing `Workloads`.

In any case, I think that transparency improves user experience. Even if the Workload is disabled, that would be great to log the event; or to have information in the status.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T12:39:19Z

Yes, we definitely want the event, the only thing is that if we deactivate then we already have a mechanism to propagate the event to the Job object, so the solution will be shorter by reusing this path, and the information will be reflected both in event and status. wdyt @tenzen-y ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:34:48Z

/kind dashboard

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:35:24Z

sorry, I think this is not directly related to dashboard
/kind-remove dashboard

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:35:48Z

/remove-kind dashboard

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-09T22:17:23Z

> Yes, we definitely want the event, the only thing is that if we deactivate then we already have a mechanism to propagate the event to the Job object, so the solution will be shorter by reusing this path, and the information will be reflected both in event and status. wdyt [@tenzen-y](https://github.com/tenzen-y) ?

Deactivating the corresponding Workload sounds reasonable. 

Batch user PoV, if we do not deactivate the Workload, and it is never admitted, it's challenging to identify the reason why their Workload is never admitted.

Cluster Admin PoV, they do not want to handle the Workload with non-existence WoriloadPriorityClass as default Priority (1) since it potentially could break priority design in the cluster.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-10T22:58:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T12:55:27Z

This looks like a still valid request.
/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-10T13:50:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T08:41:34Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-24T16:21:53Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-24T16:21:55Z

@kannon92: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3439):

>/help
>/good-first-issue
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T11:14:26Z

I'm not sure if this is a good first issue since the contributor must implement the Workload deactivation mechanism.

### Comment by [@j4ckstraw](https://github.com/j4ckstraw) — 2025-08-27T08:10:43Z

I'd like to do some work.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-27T14:53:33Z

> I'd like to do some work.

@j4ckstraw Thank you for your interest in this issue. Feel free to take this one with `/assign` comment.

### Comment by [@j4ckstraw](https://github.com/j4ckstraw) — 2025-08-28T01:26:01Z

/assign
