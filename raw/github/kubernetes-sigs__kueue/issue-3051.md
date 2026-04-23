# Issue #3051: [Flaking test] Kueue when Creating a Job With Queueing Should run with prebuilt workload

**Summary**: [Flaking test] Kueue when Creating a Job With Queueing Should run with prebuilt workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3051

**Last updated**: 2024-10-21T10:57:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-16T06:49:05Z
- **Updated**: 2024-10-21T10:57:06Z
- **Closed**: 2024-10-21T10:57:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 8

## Description

**What happened**:

The test flaked: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-28/1834993639869124608

![image](https://github.com/user-attachments/assets/0a10249d-6d17-4f8a-8b9c-50d35a0db13f)


**What you expected to happen**:

No flakes.

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the CI build.

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.28.9: [It] Kueue when Creating a Job With Queueing Should run with prebuilt workload expand_less	6s
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/e2e_test.go:185 with:
Expected
    <[]v1.OwnerReference | len:0, cap:0>: nil
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc0005792c0>: {
        Expected: <v1.OwnerReference>{
            APIVersion: "",
            Kind: "",
            Name: "test-job",
            UID: "d2e2bd31-0087-4759-a306-253b308d837f",
            Controller: nil,
            BlockOwnerDeletion: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc0006aa870>{
                core: {},
                fnc: 0x633f20,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/e2e_test.go:185 with:
Expected
    <[]v1.OwnerReference | len:0, cap:0>: nil
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc0005792c0>: {
        Expected: <v1.OwnerReference>{
            APIVersion: "",
            Kind: "",
            Name: "test-job",
            UID: "d2e2bd31-0087-4759-a306-253b308d837f",
            Controller: nil,
            BlockOwnerDeletion: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc0006aa870>{
                core: {},
                fnc: 0x633f20,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/e2e_test.go:190 @ 09/14/24 16:39:35.489
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-16T06:49:26Z

/kind flake
/cc @mbobrovskyi @trasc

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-09-16T08:45:50Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-09-18T10:49:37Z

Digging into this issue, the cause seems to be that objects came out of order. This occurs when a Workload is created after the Job that will adopt it, as shown in the logs:

```
2024-09-14T16:39:30.49936039Z stderr F 2024-09-14T16:39:30.499137821Z	LEVEL(-2)	jobframework/reconciler.go:313	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"test-job","namespace":"e2e-n4shr"}, "namespace": "e2e-n4shr", "name": "test-job", "reconcileID": "80a0f899-0e23-438a-9956-b95691055017", "job": "e2e-n4shr/test-job", "gvk": "batch/v1, Kind=Job"}
2024-09-14T16:39:30.49939532Z stderr F 2024-09-14T16:39:30.499216661Z	LEVEL(-3)	jobframework/reconciler.go:381	The workload is nil, handle job with no workload	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"test-job","namespace":"e2e-n4shr"}, "namespace": "e2e-n4shr", "name": "test-job", "reconcileID": "80a0f899-0e23-438a-9956-b95691055017", "job": "e2e-n4shr/test-job", "gvk": "batch/v1, Kind=Job"}
2024-09-14T16:39:30.49962255Z stderr F 2024-09-14T16:39:30.49943252Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:563	Workload create event	{"workload": {"name":"prebuilt-wl","namespace":"e2e-n4shr"}, "queue": "main", "status": "pending"}
```

A fix could be to set up a retry for the retrieval of the workload. However, during my test executions I found that this test seems to be flaky only on Kubernetes 1.28 which [End-of-Life is on end of October](https://kubernetes.io/releases/#release-v1-28).

@mimowo @alculquicondor WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-18T11:36:25Z

Can you investigate if this is just a test issue or it can also affect the e22 runtime?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-18T15:15:22Z

Interesting, I would think that this could happen in any k8s version. Maybe it's just very hard to reproduce in general?

In any case, it sounds like this could happen in production. The solution should be to trigger another job sync when the corresponding Workload object appears. Don't we have event handlers for that?

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-09-19T13:29:44Z

> Interesting, I would think that this could happen in any k8s version. Maybe it's just very hard to reproduce in general?
> 
> In any case, it sounds like this could happen in production. The solution should be to trigger another job sync when the corresponding Workload object appears. Don't we have event handlers for that?

Yes, we have a watcher for workloads and batch jobs, and we could do the same for jobs waiting for a prebuilt workload. Yet to do that we would need to add a watcher for every job supporting prebuilt. 

Another option would be implementing the retry because we would need to modify only the job framework reconciler.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T14:04:48Z

I think we can add an indexer into the job for the prebuilt-workload name, so that it can be used to find the job for a workload when it appears.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T08:19:15Z

Sorry for getting here only now. I think this test that flaked actually doesn't reflect production situation for MultiKueue, because it creates both Job and Workload one-by-one: https://github.com/kubernetes-sigs/kueue/blob/425ece197331d6b0c9b6d2bf4cc82326420c9f0a/test/e2e/singlecluster/e2e_test.go#L171-L172
because in MultiKueue we only create Jobs once the Workload reserved the capacity (and so needed to already exist): https://github.com/kubernetes-sigs/kueue/blob/425ece197331d6b0c9b6d2bf4cc82326420c9f0a/pkg/controller/admissionchecks/multikueue/workload.go#L351

I don't think this is 1.28 specific, it is probably just very rare that the order of processing events is different that the creation order of objects, but may happen for objects of different type.

I think we can try move forward with https://github.com/kubernetes-sigs/kueue/pull/3131, since prebuilt-workload is considered a feature on its own, but on best effort basis - if the fix becomes too complex we could resort just to adjust the test to the MK use.
