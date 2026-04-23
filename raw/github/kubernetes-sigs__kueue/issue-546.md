# Issue #546: Family of job, workload, localQueue can be in different namespaces

**Summary**: Family of job, workload, localQueue can be in different namespaces

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/546

**Last updated**: 2023-02-08T14:35:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-02-03T10:21:04Z
- **Updated**: 2023-02-08T14:35:22Z
- **Closed**: 2023-02-08T14:35:22Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If I create a localQueue lqA in ns1, then I create a job in another namespace ns2 but refers to the lqA, then we'll get a workload in ns2. Is this as expected?

**What you expected to happen**:

- localQueue should only accept jobs in the same namespace
- same to workload

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-03T10:27:52Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-03T13:27:57Z

That shouldn't happen, because we match the queues using namespace/name https://github.com/kubernetes-sigs/kueue/blob/b6bdec3bfd7427bf69af74398ddcbae4acf35d76/pkg/queue/manager.go#L274

But it would be good to have an integration/unit test for it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-04T07:50:20Z

Before https://github.com/kubernetes-sigs/kueue/pull/547, when we apply the samples in namespace, it could be like this:
```
➜  kueue git:(design/add-interface-to-kueue) ✗ (⎈ |kind-kind:kueue-system) kg job -o wide
NAME         COMPLETIONS   DURATION   AGE   CONTAINERS   IMAGES                                       SELECTOR
sample-job   0/3                      72s   dummy-job    gcr.io/k8s-staging-perf-tests/sleep:latest   controller-uid=403bc6ea-bed2-4054-97d8-3bd25fc35e7c
➜  kueue git:(design/add-interface-to-kueue) ✗ (⎈ |kind-kind:kueue-system) kg workloads -o wide
NAME         QUEUE   ADMITTED BY   AGE
sample-job   main                  77s
➜  kueue git:(design/add-interface-to-kueue) ✗ (⎈ |kind-kind:kueue-system) kg queue -A
NAMESPACE   NAME   CLUSTERQUEUE    PENDING WORKLOADS   ADMITTED WORKLOADS
default     main   cluster-total   0                   0
➜  kueue git:(design/add-interface-to-kueue) ✗ (⎈ |kind-kind:kueue-system)
```
~The job and the workload located in `kueue-system` namespace, but the localQueue is in the `default` namespace.~

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-04T07:56:24Z

Oh, I think I misunderstood it, different namespaces can have different localQueues with the same queueName, so it doesn't matter. Still working good. Sorry for the disturbing, let me see whether this worths a integration test.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-04T07:56:54Z

/remove-kind bug
/kind cleanup
