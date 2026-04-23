# Issue #1651: ClusterQueue admitted a workload after set stopPolicy to Hold

**Summary**: ClusterQueue admitted a workload after set stopPolicy to Hold

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1651

**Last updated**: 2024-02-07T03:52:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@B1F030](https://github.com/B1F030)
- **Created**: 2024-01-26T10:20:13Z
- **Updated**: 2024-02-07T03:52:19Z
- **Closed**: 2024-02-07T03:52:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
I submitted 3 jobs first: 1 `Running`, 1 `Pending`, 1 `Not Admitted`.
```
=============submitting 3 jobs===============
job.batch/sample-job-82xff created
job.batch/sample-job-rxgl6 created
job.batch/sample-job-p9tb6 created
=====================pod=====================
NAME                     READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
sample-job-82xff-8vfnq   1/1     Running   0          7s    10.233.123.41    test-2   <none>           <none>
sample-job-82xff-rjd2h   1/1     Running   0          7s    10.233.125.166   test-1   <none>           <none>
sample-job-rxgl6-ch72s   0/1     Pending   0          5s    <none>           <none>   <none>           <none>
sample-job-rxgl6-dsxfb   0/1     Pending   0          5s    <none>           <none>   <none>           <none>
==================workload===================
NAME                         QUEUE          ADMITTED BY   AGE
job-sample-job-82xff-ddd56   team-a-queue   team-a-cq     7s
job-sample-job-p9tb6-5ef3f   team-a-queue                 3s
job-sample-job-rxgl6-e6970   team-a-queue   team-a-cq     5s
=================localqueue==================
NAME                  CLUSTERQUEUE       PENDING WORKLOADS   ADMITTED WORKLOADS
team-a-queue          team-a-cq          1                   2
team-b-queue          team-b-cq          0                   0
```
Then I updated `team-a-cq` to `stopPolicy`: `Hold`.
After some time:
the first job went from `Running` to `Completed`;
the second job went from `Pending` to `Running`, then `Completed`;
and the third job also went from `Not Admitted` to `Pending`, then `Running`, at last `Completed`;
```
==================workload===================
NAME                         QUEUE          ADMITTED BY   AGE
job-sample-job-82xff-ddd56   team-a-queue   team-a-cq     77s
job-sample-job-p9tb6-5ef3f   team-a-queue   team-a-cq     73s
job-sample-job-rxgl6-e6970   team-a-queue   team-a-cq     75s
```


**What you expected to happen**:
I just wonder, if this is a bug, or it is so designed?
Because it is described like this in the KEP:
```
type ClusterQueueSpec struct {
	// stopPolicy - if set the ClusterQueue is considered Inactive, no new reservation being
	// made. 
	//
	// Depending on its value, its associated workloads will:
	//
	// - None - Workloads are admitted
	// - HoldAndDrain - Admitted workloads are evicted and Reserving workloads will cancel the reservation.
	// - Hold - Admitted workloads will run to completion and Reserving workloads will cancel the reservation.
	StopPolicy StopPolicy `json:"stopPolicy,omitempty"`
}
```
I'm not sure if `Reserving workloads will cancel the reservation` means that `Not Admitted` jobs should be admitted or not.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-rc.1-5-g1adca15-dirty
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T10:10:19Z

/cc @trasc 
To take a look as the author of https://github.com/kubernetes-sigs/kueue/commit/4d7f990ca30c831ccd43f7d9e15be481f184d304

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-05T14:49:55Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-02-06T15:53:52Z

@B1F030 I'm unable to reproduce the described scenario described, can you try using the unmodified example files and :

1. cerate 9 jobs from `examples/jobs/sample-job.yaml` (they should fit 3 at a time )
2. witnin a 30s window , update the cluster-kueue (`stopPolicy: Hold`)
3. check the number of completed jobs after 90s
(only 3 should be completed)

Thanks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-06T16:06:27Z

> and the third job also went from Not Admitted to Pending, then Running, at last Completed;

this doesn't sound like working as intended.

`Hold` means that no more jobs should be admitted. The "pending" job is already admitted, so it should run to completion.

### Comment by [@B1F030](https://github.com/B1F030) — 2024-02-07T03:52:18Z

Oh, in my environment, I set the nominalQuota bigger than actual quota, so that feels wrong.
After I change the quota to actual limit, that works as expected:
```
=============================================
[KEP-1284] A mechanism to stop a ClusterQueue
=============submitting 2 jobs===============
job.batch/sample-job-jd5xb created
job.batch/sample-job-hg2ms created
=====================pod=====================
NAME                     READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
sample-job-jd5xb-lf697   1/1     Running   0          4s    10.233.123.196   test-2   <none>           <none>
==================workload===================
NAME                         QUEUE          ADMITTED BY   AGE
job-sample-job-hg2ms-bea37   team-b-queue                 2s
job-sample-job-jd5xb-929ef   team-b-queue   team-b-cq     4s
=================localqueue==================
NAME                  CLUSTERQUEUE       PENDING WORKLOADS   ADMITTED WORKLOADS
best-effort-a-queue   best-effort-a-cq   0                   0
best-effort-b-queue   best-effort-b-cq   0                   0
local-queue           cluster-queue      0                   0
shared-queue          shared-cq          0                   0
standard-a-queue      standard-a-cq      0                   0
standard-b-queue      standard-b-cq      0                   0
team-a-queue          team-a-cq          0                   0
team-b-queue          team-b-cq          1                   1
=============================================
[updating team-b-cq to stopPolicy: Hold]
=============================================
clusterqueue.kueue.x-k8s.io/team-b-cq patched
=============================================
NAME                  CLUSTERQUEUE       PENDING WORKLOADS   ADMITTED WORKLOADS
best-effort-a-queue   best-effort-a-cq   0                   0
best-effort-b-queue   best-effort-b-cq   0                   0
local-queue           cluster-queue      0                   0
shared-queue          shared-cq          0                   0
standard-a-queue      standard-a-cq      0                   0
standard-b-queue      standard-b-cq      0                   0
team-a-queue          team-a-cq          0                   0
team-b-queue          team-b-cq          1                   1
==================workload===================
NAME                         QUEUE          ADMITTED BY   AGE
job-sample-job-hg2ms-bea37   team-b-queue                 8s
job-sample-job-jd5xb-929ef   team-b-queue   team-b-cq     10s
===========submitting a new job==============
job.batch/sample-job-6lgkq created
==================workload===================
NAME                         QUEUE          ADMITTED BY   AGE
job-sample-job-6lgkq-88dfd   team-b-queue                 3s
job-sample-job-hg2ms-bea37   team-b-queue                 71s
job-sample-job-jd5xb-929ef   team-b-queue   team-b-cq     73s
=============================================
job.batch "sample-job-6lgkq" deleted
job.batch "sample-job-hg2ms" deleted
job.batch "sample-job-jd5xb" deleted
clusterqueue.kueue.x-k8s.io/team-b-cq patched
=============================================
```
As expected, the workload `Not Admitted` will not be admitted after the `stopPolicy` set to `Hold`.
Thanks for the explanation! I'll close this issue as resolved, sorry for my mistake.
