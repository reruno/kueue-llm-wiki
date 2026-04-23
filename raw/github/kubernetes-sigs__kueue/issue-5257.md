# Issue #5257: [Discussion]: In Place Pod Resizing and Kueue

**Summary**: [Discussion]: In Place Pod Resizing and Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5257

**Last updated**: 2026-02-02T12:50:24Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-05-15T14:46:08Z
- **Updated**: 2026-02-02T12:50:24Z
- **Closed**: 2026-02-01T00:27:42Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 20

## Description

Kubernetes has a feature called in place pod resizing which would relax immutability of pods. Users can be able to resize pods for core resources.

I think this could be a potential way to bypass Kueue quota.

Imagine the following scenario:

a) User admits a workload with low memory/cpu requests.
b) workload is admitted and scheduled.
c) User resizes workload to much larger memory/cpu request.
d) Workload will use more resources than Kueue admitted.


This is maybe less of a concern for cpu/memory but I think this could be a bigger issue if/when in place provides support for extended resources (people could get more gpus than Kueue allows).

## Short Term Fixes

We could document that in place pod resizing and Kueue will not play nice together and recommend disabling resize resource for batch-users?

## Long Term Fixes

Maybe Kueue should be aware of resizing requests and evict the workload and readmit?

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T14:46:29Z

cc @tallclair as in place pod SME.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T14:48:50Z

Thank you for opening this issue. I know this feature was graduated to Beta in 1.33. So, we absolutely need to consider this.
This is similar requirements with DynamicJob supports in Kueue, I guess.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T14:49:02Z

/kind discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-15T14:49:05Z

@tenzen-y: The label(s) `kind/discussion` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5257#issuecomment-2884108411):

>/kind discussion


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T14:49:17Z

/kind feature

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T15:10:06Z

cc @mwielgus @mwysokin

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-05-15T15:14:47Z

@kannon92 @tenzen-y @mimowo What if we re-adjust and the proposed long-term fix would become a middle-term one and a proper long-term fix would be in-place quota adjustment to reflect the pod resize request?

Would that be even possible considering the current implementation of quota assignment?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T15:21:33Z

> What if we re-adjust and the proposed long-term fix would become a middle-term one and a proper long-term fix would be in-place quota adjustment to reflect the pod resize request?

Indeed, evicting and re-admitting the workload might be already working (could you check @kannon92 ?). I think it would work, because Kueue has a generic mechanism of comparing the recorded PodTemplate (at the moment of admission) in the workload object with the PodTemplate when the job is running. If there are changes, the workload gets evicted to prevent changes post admitting.

I also think that the long-term solution would be to somehow adjust quota without preempting the workload. Scale down looks relatively easy.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T15:24:17Z

So to be clear, this would only impact naked pod integration ATM. I don't think workloads (Job, Deployment, StatefulSet) have relaxed the immutability of PodTemplate.

I thought we wouldn't reschedule pod workloads? If a pod gets evicted then it would not be recreated unless it was part of workload?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-20T20:58:09Z

@iholder101 brought this up to sig-node on May 20th.

The best summary of this is https://github.com/kubernetes/kubernetes/issues/131835#issuecomment-2893651171.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-21T03:25:47Z

@mimowo is correct. It looks like kueue removes a pod if spec is different from what it expects.

reproduction:

```yaml
apiVersion: v1
kind: Pod
metadata:
  generateName: kueue-sleep-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  containers:
  - name: nginx
    image: registry.k8s.io/nginx-slim:0.27
    ports:
      - containerPort: 80
    resources:
      requests:
        cpu: "100m"
        memory: "1G"
    resizePolicy:
    - resourceName: cpu
      restartPolicy: NotRequired # Default, but explicit here
    - resourceName: memory
      restartPolicy: RestartContainer
  restartPolicy: OnFailure
```

Using kubernetes 1.33 with kubectl 1.33,

Pod is scheduled and running.

I then run `kubectl patch pod kueue-sleep-cj6vh --subresource resize --patch '{"spec":{"containers":[{"name":"nginx", "resources":{"requests":{"memory":"2G"}, "limits":{"memory":"2G"}}}]}}'`

I see the following events:

```
2s          Normal    Created                   pod/kueue-sleep-cj6vh                  Created container: nginx
2s          Normal    Started                   pod/kueue-sleep-cj6vh                  Started container nginx
3s          Normal    Killing                   pod/kueue-sleep-cj6vh                  Container nginx resize requires restart
2s          Normal    Stopped                   pod/kueue-sleep-cj6vh                  No matching Workload; restoring pod templates according to existent Workload
2s          Normal    DeletedWorkload           pod/kueue-sleep-cj6vh                  Deleted not matching Workload: default/pod-kueue-sleep-cj6vh-52863
2s          Normal    Killing                   pod/kueue-sleep-cj6vh                  Stopping container nginx
```

Pod is killed after the resize and not admitted. So it sounds like we handle this actually!  Neat!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-19T04:05:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:45:14Z

/remove-lifecycle stale

### Comment by [@tallclair](https://github.com/tallclair) — 2025-09-03T22:38:54Z

/cc @natasha41575

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-02T23:03:26Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-01T23:38:12Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-01T00:27:37Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-01T00:27:43Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5257#issuecomment-3829833935):

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

### Comment by [@iholder101](https://github.com/iholder101) — 2026-02-02T06:01:53Z

FYI that this is closed and the in-place feature is GAed in 1.35.
Were there any developments on this issue?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-02T12:50:24Z

Other than my research into that Kueue evicts pods if they change after being admitted, nothing else has been done.
