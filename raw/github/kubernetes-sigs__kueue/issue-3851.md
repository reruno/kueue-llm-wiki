# Issue #3851: Workload active field doesn't work for StatefulSet for Notebook Integration

**Summary**: Workload active field doesn't work for StatefulSet for Notebook Integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3851

**Last updated**: 2025-07-24T22:20:57Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@xiongzubiao](https://github.com/xiongzubiao)
- **Created**: 2024-12-14T02:13:31Z
- **Updated**: 2025-07-24T22:20:57Z
- **Closed**: 2025-07-24T22:20:56Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@varshaprasad96](https://github.com/varshaprasad96)
- **Comments**: 19

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Changing the `active` field of the Workload object from true to false doesn't scale down the StatefulSet permanently in v0.10.0-rc.4. It only temporarily change the status. Both the workload object and the pods are deleted but immediately recreated automatically.

**What you expected to happen**:
Changing the `active` field from true to false should scale the StatefulSet down to 0. Changing it back to true should scale up the StatefulSet.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31.0
- Kueue version (use `git describe --tags --dirty --always`): v0.10.0-rc.4
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T06:19:33Z

it needs testing but I think adding the StatefulSet to the owners of the Workload will prevent workload deletion and so it should work well.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-16T19:00:04Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T09:52:53Z

> it needs testing but I think adding the StatefulSet to the owners of the Workload will prevent workload deletion and so it should work well.

It won't help because the workload could still finish. I think we need to add a "serving" field to the workload to prevent it from finishing.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T10:19:38Z

> It won't help because the workload could still finish. 

Could you please that approach first. It is possible that I'm missing something, but I think we need to keep the workload around. Also, it is not clear to me why we need the "serving" field on workload since it is already on the pods created by StatefulSet. In any case, the argument is not convincing to me yet.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T11:14:13Z

The problem is that the workload finishes once all the pods are finished. Yes, with the ownerReference, the workload won't disappear, but we can't admit it after reactivation.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T13:14:22Z

Preventing the workload from disappearing is the first step - if it is gone, then for sure "active" is gone too. 

Yes, possibly we may need the "serving" field on workload, but I would prefer to reuse the pod annotation so that we can cherry-pick the fix for 0.10.1. So, I would prefer to first understand well where are the issues, rather than jumping to conclusions.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T13:16:58Z

Moreover, starting with ownerReferences would fix the issue already for workloads which return non-zero exit code on SIGTERM, which would already unblock the use case for some users.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T14:31:19Z

/unassign

Sorry, I don't have capacity to work on it.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-12-17T16:50:28Z

@mbobrovskyi I can work on it after the holidays. 

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T07:57:01Z

@varshaprasad96 any progress on that? It is not top priority, but would be great to include the fix for 0.11.0 which is planned mid March: https://github.com/kubernetes-sigs/kueue/issues/4249.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-02-13T22:09:39Z

I haven't had the bandwidth to work on this yet, but planning to do so next week. Will make sure to get a PR soon.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-02-20T22:01:31Z

@mimowo @mbobrovskyi - Adding StatefulSet as an ownerRef does not quite solve the issue in here. Since the statefulset is being controlled by the notebook controller in turn, modifying the workload spec does not quite do the trick as the notebook controller reconciles it to scale the SS up again. 

To explain the sequence of events:
```
0s          Normal   FinishedWorkload          notebook/notebook-sample-v1                     Reissued from pod/notebook-sample-v1-0: Workload 'notebook/statefulset-notebook-sample-v1-6fdb1' is declared finished
0s          Normal   FinishedWorkload          pod/notebook-sample-v1-0                        Workload 'notebook/statefulset-notebook-sample-v1-6fdb1' is declared finished
0s          Normal   OwnerReferencesAdded      workload/statefulset-notebook-sample-v1-6fdb1   Added 1 owner reference(s)
0s          Normal   FinishedWorkload          pod/notebook-sample-v1-0                        Workload 'notebook/statefulset-notebook-sample-v1-6fdb1' is declared finished
0s          Normal   SuccessfulCreate          statefulset/notebook-sample-v1                  create Pod notebook-sample-v1-0 in StatefulSet notebook-sample-v1 successful
0s          Normal   CreatedWorkload           pod/notebook-sample-v1-0                        Created Workload: notebook/statefulset-notebook-sample-v1-6fdb1
0s          Normal   QuotaReserved             workload/statefulset-notebook-sample-v1-6fdb1   Quota reserved in ClusterQueue cluster-queue, wait time since queued was 0s
0s          Normal   Admitted                  workload/statefulset-notebook-sample-v1-6fdb1   Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s
```

1. Once we modify the workload's active field to be `false`, the SS does scale down and pods get deleted. 
2. The notebook controller kicks in and scales up the SS again to ensure it's in accordance with what's specified in the NB CR.

```
1.7400882340742986e+09	INFO	controllers.Notebook	Reconciliation loop started	{"notebook": "notebook/notebook-sample-v1"}
1.7400882340743833e+09	INFO	controllers.Notebook	Updating StatefulSet	{"notebook": "notebook/notebook-sample-v1", "namespace": "notebook", "name": "notebook-sample-v1"}
1.7400882340858157e+09	INFO	controllers.Notebook	Initializing Notebook CR Status	{"notebook": "notebook/notebook-sample-v1"}
1.7400882340858355e+09	INFO	controllers.Notebook	Calculating Notebook's  containerState	{"notebook": "notebook/notebook-sample-v1"}
```
3. The Workload is set to active again.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-02-20T22:08:52Z

Thinking about it a bit more - to be able to control scaling up of SS through the WL API, we should be modifying the NB CR spec instead to ensure that Notebook controller does not reconcile and get it back to the previous state. This is not in the scope of Kueue to do it.

In case the users would like to stop the Notebooks, they should use the pause feature present in the Notebook controller itself, which is annotating the CR:

```
k annotate notebook/notebook-sample-v1 kubeflow-resource-stopped="true" -n notebook 
```

This scales down the SS, and deletes the pod, with the side-effect of deleting the workload too.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T10:40:41Z

@varshaprasad96 thank you for looking into this, and let me ask some questions:

> Once we modify the workload's active field to be false, the SS does scale down and pods get deleted.

Actually, why does the SS scale down? I would imagine setting `active=false` should allow for the STS to delete all Pods, but keep the Workload existing, and do not scale the SS. Similarly as the newly created STS has replicas >0, and remains suspended. Still, scaling down at this point is probably ok-ish still.

Note that when the `active is set to false` Kueue releases the quota, and re-admission is necessary. To trigger deletion of pods we may need to implement `Stop` for the STS which injects Kueue annotation to the STS Pod Template,, say `kueue.x-k8s.io/sts-stopped-at: <datetime>`.

> The notebook controller kicks in and scales up the SS again to ensure it's in accordance with what's specified in the NB CR.

This scale-up should not be necessary IMO, if we keep the size unchanged.

> The Workload is set to active again.

Which entity changes to active again actually? I guess NB controller could be doing this.

Overall, there are two things to follow up on IMO:
1. figure out if the integration can be improved and if the scale down / up are needed at all. I believe modifying the active field could be enough. Scale down / up to 0 is another approach which should work.
2. I believe regardless of the integration there is a bug in Kueue, we may track it independently, that the workload is deleted after setting `active=false`. This should be fixed by adding the owner reference to the STS IMO.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T11:26:10Z

Created dedicated issue about the field https://github.com/kubernetes-sigs/kueue/issues/4342 to de-couple it from the Notebook integration. I believe also this issue might be complicating interpretation of the results for the integration.

Let me retitle this one to focus on Notebook integration specicailly.
/retitle Workload active field doesn't work for StatefulSet for Notebook Integration

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-22T11:34:53Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-24T22:04:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-24T22:20:51Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-24T22:20:56Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3851#issuecomment-3115170084):

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
