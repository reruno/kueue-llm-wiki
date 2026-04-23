# Issue #8635: TAS: MPIJob PodSet Group Rank-based ordering doesn't work correctly

**Summary**: TAS: MPIJob PodSet Group Rank-based ordering doesn't work correctly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8635

**Last updated**: 2026-02-14T22:03:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-16T13:05:53Z
- **Updated**: 2026-02-14T22:03:48Z
- **Closed**: 2026-02-14T22:02:31Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When I deployed runLauncherAsWorker MPIJob with PodSet Group, the nodes are randomly assigned to Pods as you can see in the following. 

```shell
NAME                                   READY   STATUS      RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
ranks-mpi-podsetgroup-launcher-d52xq   0/1     Completed   0          2m43s   10.244.7.2   kind-worker2   <none>           <none>
ranks-mpi-podsetgroup-worker-0         0/1     Completed   0          2m43s   10.244.7.3   kind-worker2   <none>           <none>
ranks-mpi-podsetgroup-worker-1         0/1     Completed   0          2m43s   10.244.4.4   kind-worker3   <none>           <none>
ranks-mpi-podsetgroup-worker-2         0/1     Completed   0          2m43s   10.244.5.4   kind-worker4   <none>           <none>
```

**What you expected to happen**:
Expected assignments are the following:

- "launcher": "kind-worker"
- "worker-0": "kind-worker-2"
- "worker-1": "kind-worker-3"
- "worker-2": "kind-worker-4"

**How to reproduce it (as minimally and precisely as possible)**:
I verified that this could be reproducible in our E2E test. 

- Verified PR: https://github.com/kubernetes-sigs/kueue/pull/8630
- Verified CI Job Log: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8630/pull-kueue-test-e2e-tas-main/2012128250033082368

```go
{Expected object to be comparable, diff:   map[string]string{
-   "launcher/0": "kind-worker",
+   "launcher/0": "kind-worker2",
-   "worker/1":   "kind-worker2",
+   "worker/1":   "kind-worker",
-   "worker/2":   "kind-worker3",
+   "worker/2":   "kind-worker2",
-   "worker/3":   "kind-worker4",
+   "worker/3":   "kind-worker3",
  }
 failed [FAILED] Expected object to be comparable, diff:   map[string]string{
-   "launcher/0": "kind-worker",
+   "launcher/0": "kind-worker2",
-   "worker/1":   "kind-worker2",
+   "worker/1":   "kind-worker",
-   "worker/2":   "kind-worker3",
+   "worker/2":   "kind-worker2",
-   "worker/3":   "kind-worker4",
+   "worker/3":   "kind-worker3",
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/mpijob_test.go:228 @ 01/16/26 12:03:23.316
}
```

- Verified MPIJob:

```yaml
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  labels:
    kueue.x-k8s.io/queue-name: local-queue
  name: ranks-mpi-podsetgroup
  namespace: e2e-tas-mpijob-k5zkv
spec:
  launcherCreationPolicy: AtStartup
  mpiImplementation: OpenMPI
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-group-name: same-group
            kueue.x-k8s.io/podset-required-topology: cloud.provider.com/topology-block
        spec:
          containers:
          - args:
            - entrypoint-tester
            image: registry.k8s.io/e2e-test-images/agnhost:2.59
            name: mpijob
            resources:
              limits:
                example.com/gpu: "1"
              requests:
                example.com/gpu: "1"
          restartPolicy: OnFailure
    Worker:
      replicas: 3
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-group-name: same-group
            kueue.x-k8s.io/podset-required-topology: cloud.provider.com/topology-block
        spec:
          containers:
          - args:
            - entrypoint-tester
            image: registry.k8s.io/e2e-test-images/agnhost:2.59
            name: mpijob
            resources:
              limits:
                example.com/gpu: "1"
              requests:
                example.com/gpu: "1"
          restartPolicy: OnFailure
  runLauncherAsWorker: true
  runPolicy:
    suspend: false
  slotsPerWorker: 1
  sshAuthMountPath: /root/.ssh
```

**Anything else we need to know?**:

The created Workload is the following:

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  labels:
    kueue.x-k8s.io/job-uid: 3c7a6666-efaa-4adc-bd81-8a30fa5a04a0
  name: mpijob-ranks-mpi-podsetgroup-cf81d
  namespace: e2e-tas-mpijob-k5zkv
spec:
  active: true
  podSets:
  - count: 1
    name: launcher
    template: {...}
    topologyRequest:
      podIndexLabel: training.kubeflow.org/replica-index
      podSetGroupName: same-group
      required: cloud.provider.com/topology-block
  - count: 3
    name: worker
    template: {...}
    topologyRequest:
      podIndexLabel: training.kubeflow.org/replica-index
      podSetGroupName: same-group
      required: cloud.provider.com/topology-block
  priority: 0
  queueName: local-queue
status:
  admission:
    clusterQueue: cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        example.com/gpu: tas-flavor
      name: launcher
      resourceUsage:
        example.com/gpu: "1"
      topologyAssignment:
        levels:
        - kubernetes.io/hostname
        slices:
        - domainCount: 1
          podCounts:
            universal: 1
          valuesPerLevel:
          - universal: kind-worker
    - count: 3
      flavors:
        example.com/gpu: tas-flavor
      name: worker
      resourceUsage:
        example.com/gpu: "3"
      topologyAssignment:
        levels:
        - kubernetes.io/hostname
        slices:
        - domainCount: 3
          podCounts:
            universal: 1
          valuesPerLevel:
          - individual:
              prefix: kind-worker
              roots:
              - "2"
              - "3"
              - "4"
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T13:10:17Z

This LWS TAS E2E test is similar to the MPIJob TAS failed test (https://github.com/kubernetes-sigs/kueue/pull/8630)

https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/test/e2e/tas/leaderworkerset_test.go#L170-L277

I'm wondering why only LWS could work well 🤔

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T13:20:38Z

It might be unrelated, but this snippet made me wondering if we handle correctly in the TAS v1beta2 the case when one of the node names is a prefix for others, like here:

```yaml
topologyAssignment:
  levels:
  - kubernetes.io/hostname
  slices:
  - domainCount: 3
    podCounts:
      universal: 1
    valuesPerLevel:
    - individual:
        prefix: kind-worker
        roots:
        - "2"
        - "3"
        - "4"
```
where the nodes are `kind-worker`, `kind-worker2`, `kind-worker3`, `kind-worker4`. This should not happen for any of the known cloud provider schemes, so maybe we overlooked, but it may happen well on kind. 

Let me cc @olekzabl here

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T13:25:44Z

> where the nodes are kind-worker, kind-worker2, kind-worker3, kind-worker4. This should not happen for any of the know cloud provider schemes, so maybe we overlooked, but it may happen well on kind.

Uhm, good point. Yes, that might be unrelated, but I think that verifying would be worth it if a kind cluster name pattern could work correctly. I guess that we might be able to create a new issue to track verification.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T13:29:51Z

Opened: https://github.com/kubernetes-sigs/kueue/issues/8636

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-16T13:30:13Z

@mimowo @tenzen-y I _think_ there's no bug like this in the new TAS format, as I don't see anything that would reject empty items on the [`Roots` list](https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/apis/kueue/v1beta2/workload_types.go#L487-L494). 

But I agree this should be verified. (Most likely, by an e2e test).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T13:33:57Z

> [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) I _think_ there's no bug like this in the new TAS format, as I don't see anything that would reject empty items on the [`Roots` list](https://github.com/kubernetes-sigs/kueue/blob/3250572ddbdc351dc27f73f70b713822abed1cc5/apis/kueue/v1beta2/workload_types.go#L487-L494).
> 
> But I agree this should be verified. (Most likely, by an e2e test).

Thank you for letting us know. Yes, verification by test would be worth it 👍

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T21:57:44Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T22:01:46Z

As I checked this problem more deeply, I found that this is not Kueue problem and this is caused by MPIOperator bug reported in https://github.com/kubernetes-sigs/kueue/issues/3400

Even when Kueue assigns flavors and unsuspend MPIJob, MPI Operator doesn't update Launcher Job at all. So, created batch/v1 Job and Pods don't have accurately Labels / Annotations / NodeSelectors, ... which means all fields are incorrect 😓 

Because of this problem, the TAS couldn't work well.

SIDE NOTE: Worker Pods assignments (both flavor and TAS) are correct because worker Pods are directly created by the MPI Operator instead of via batch/v1 Job.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T22:02:27Z

Let me close this issue and move the discussion to #3400.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-14T22:02:32Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8635#issuecomment-3902621943):

>Let me close this issue and move the discussion to #3400.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
