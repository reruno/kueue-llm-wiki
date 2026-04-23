# Issue #1574: [Discussion] Consider pytorchJob cleanPodPolicy in kueue

**Summary**: [Discussion] Consider pytorchJob cleanPodPolicy in kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1574

**Last updated**: 2024-06-04T06:03:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2024-01-12T06:50:31Z
- **Updated**: 2024-06-04T06:03:35Z
- **Closed**: 2024-06-04T06:03:33Z
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 8

## Description

```
[root@flavor-1 yaml]# kubectl get pytorchjobs.kubeflow.org 
NAME                   STATE       AGE
pytorch-simple-td5kx   Succeeded   35s
```

```
[root@flavor-1 yaml]# kubectl get pod -o wide
NAME                            READY   STATUS      RESTARTS   AGE     IP              NODE       NOMINATED NODE   READINESS GATES
pytorch-simple-td5kx-master-0   0/1     Completed   0          2m31s   10.233.66.243   flavor-1   <none>           <none>
pytorch-simple-td5kx-worker-0   1/1     Running     0          2m31s   10.233.66.244   flavor-1   <none>           <none>
pytorch-simple-td5kx-worker-1   1/1     Running     0          2m31s   10.233.67.157   flavor-2   <none>           <none>
pytorch-simple-td5kx-worker-2   1/1     Running     0          2m31s   10.233.66.245   flavor-1   <none>           <none>
```

```
[root@flavor-1 yaml]# kubectl get localqueues.kueue.x-k8s.io local-queue -oyaml | grep flavorUsage -A 15
  flavorUsage:
  - name: default-flavor
    resources:
    - name: cpu
      total: "0"
  flavorsReservation:
  - name: default-flavor
    resources:
    - name: cpu
      total: "0"
  pendingWorkloads: 0
  reservingWorkloads: 0
```

With `spec.runPolicy.cleanPodPolicy=Running` unset, when job succeeds, the workers may still keep running, but kueue will reclaim the whole resources, which seems not rigorous. 

A better way seems like we should reclaim the completed pods rather than the whole job, but the tricky thing is it's hard for the kueue to aware of the individual Pods. At least, we should shout out this limitations.

## Discussion

### Comment by [@asm582](https://github.com/asm582) — 2024-01-15T14:45:07Z

"A better way seems like we should reclaim the completed pods rather than the whole job, but the tricky thing is it's hard for the kueue to aware of the individual Pods. At least, we should shout out this limitations."

Can you specify the use case to borrow individual pods, is it for borrowing/autoscaling use case?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2024-01-24T05:39:58Z

A tangental question: why use pytorchJob in the first place? I imagine Indexed Job to work better for pytorch training.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-24T08:22:00Z

> Can you specify the use case to borrow individual pods, is it for borrowing/autoscaling use case?

What I mean is Kueue should be aware of the completed pods of pytorchJob, I think this can be supported by the job interface `JobWithReclaimablePods` of kueue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-24T08:29:13Z

> A tangental question: why use pytorchJob in the first place? I imagine Indexed Job to work better for pytorch training.

Some of our customers still use pytorchJob now, migrations could be additional work to them. But I think pytorchJob still plays well at some place, elastic for example.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-03-06T03:08:15Z

cc @B1F030

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-04T03:48:29Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-06-04T06:03:30Z

/close

close as not planned.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-04T06:03:34Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1574#issuecomment-2146679881):

>/close
>
>close as not planned.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
