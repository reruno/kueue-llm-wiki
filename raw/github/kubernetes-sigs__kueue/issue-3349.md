# Issue #3349: JobSet stays in suspend state if kueue is managing it

**Summary**: JobSet stays in suspend state if kueue is managing it

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3349

**Last updated**: 2024-10-30T07:53:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-10-28T19:24:51Z
- **Updated**: 2024-10-30T07:53:51Z
- **Closed**: 2024-10-30T04:13:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 18

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
If I submit a simple JobSet with kueue, the workload stays in a suspend state.
**What you expected to happen**:
Kueue will unsuspend and the workload will run successfully.

**How to reproduce it (as minimally and precisely as possible)**:

```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: paralleljobs
  namespace: kueue-demo
  labels:
    kueue.x-k8s.io/queue-name: queue
spec:
  replicatedJobs:
  - name: workers
    replicas: 2
    template:
      spec:
        parallelism: 4
        completions: 4
        backoffLimit: 0
        template:
          spec:
            containers:
            - name: sleep
              image: quay.io/quay/busybox
              command: 
                - sleep
              args:
                - 100s
  - name: driver
    template:
      spec:
        parallelism: 1
        completions: 1
        backoffLimit: 0
        template:
          spec:
            containers:
            - name: sleep
              image: quay.io/quay/busybox
              command: 
                - sleep
              args:
                - 100s

```

1) Submit a jobset that uses kueue (ie add  Workload will stay in a suspended state.

**Anything else we need to know?**:
JobSet is 0.7.0.
**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): 0.8.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-28T19:28:05Z

Workload says its admitted;

```
kueue$ oc get workloads -n kueue-demo
NAME                         QUEUE   RESERVED IN     ADMITTED   FINISHED   AGE
job-sample-job-55pkz-a624b   queue   cluster-queue   True       True       20m
jobset-paralleljobs-b13e4    queue   cluster-queue   True                  12m
```

But the jobset is suspended:

```
kehannon@kehannon-thinkpadp1gen4i:~/Work/openshift/kubecon-na-2024/kueue$ oc get jobset -n kueue-demo
NAME           TERMINALSTATE   RESTARTS   COMPLETED   SUSPENDED   AGE
paralleljobs                                          true        13m
```

If I submit this jobSet without the kueue label, the workload runs without issue.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-28T19:36:03Z

```
"error":"JobSet.jobset.x-k8s.io \"paralleljobs\" is invalid: spec.network: Invalid value: \"object\": Value is immutable","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:227"}
```

Kueue manager logs are logging this error.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T04:36:35Z

We already fixed https://github.com/kubernetes-sigs/kueue/pull/3132 on 0.9.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T04:37:12Z

@mimowo @tenzen-y maybe we should cherry-pick to 0.8?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T06:11:13Z

I think it might be a good idea indeed. The fix does not require API changes. We deferred due to possibly many conflicts but I think it is worth trying. 

Could you please try to prepare a minimal cherry - pick so that we can assess what it entails?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T06:12:53Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T07:45:35Z

OK. On this case I think we need to cherry-pick https://github.com/kubernetes-sigs/kueue/pull/3102 and https://github.com/kubernetes-sigs/kueue/pull/3132

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T07:52:26Z

> I think it might be a good idea indeed. The fix does not require API changes. We deferred due to possibly many conflicts but I think it is worth trying.
> 
> Could you please try to prepare a minimal cherry - pick so that we can assess what it entails?

SGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T07:53:15Z

I think I'm ok with with that - no API / schema changes in the diffs, but the changes are big, so let me confirm with @tenzen-y .  Actually, we discussed the cherry-picking before and the main argument was that we still have time before release of new CRDs, which is proven wrong by the issue. 

OTOH, we are just a week from releasing 0.9.0, and based on the comment https://github.com/kubernetes-sigs/kueue/issues/3349#issuecomment-2443192999 @kannon92 could probably mitigate by using 0.9.0-rc.1

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T08:02:59Z

> I think I'm ok with with that - no API / schema changes in the diffs, but the changes are big, so let me confirm with @tenzen-y . Actually, we discussed the cherry-picking before and the main argument was that we still have time before release of new CRDs, which is proven wrong by the issue.
> 
> OTOH, we are just a week from releasing 0.9.0, and based on the comment [#3349 (comment)](https://github.com/kubernetes-sigs/kueue/issues/3349#issuecomment-2443192999) @kannon92 could probably mitigate by using 0.9.0-rc.1

Yes, that's right. However, the discussion result was based on the already resolved RayJob issue.
So, based on this JobSet issue, we might want to cherry-pick. Or, we may be able to just upgrade the JobSet version in the release-0.8 branch.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T08:13:05Z

> Or, we may be able to just upgrade the JobSet version in the release-0.8 branch.

This could be an option indeed. If this is less changes I'm ok to also start with that

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T08:14:52Z

@mbobrovskyi, Could you check if we can upgrade the JobSet module version with fewer changes?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-29T08:18:58Z

> @mbobrovskyi, Could you check if we can upgrade the JobSet module version with fewer changes?

Ah, it's require to upgrade the Kubernetes version to v0.31.1. And there are a lot of changes :)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T08:21:22Z

 in that case let's go with the fix for field dropping

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-29T13:22:03Z

Thank you all! My hope was to test Kueue with released containers for Kubecon so using the rc isn’t ideal.

Either way I think having this change for 0.8 will be useful as 0.9 requires 1.31 so this will be helpful.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-30T04:13:32Z

/close

Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/3358.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-30T04:13:37Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3349#issuecomment-2445802493):

>/close
>
>Due to fixed on https://github.com/kubernetes-sigs/kueue/pull/3358.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-30T07:53:50Z

FYI we are going to release 0.8.2 which will include the fix: https://github.com/kubernetes-sigs/kueue/issues/3371
