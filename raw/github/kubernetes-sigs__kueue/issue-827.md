# Issue #827: Workload is not admitted after upgrading from kueue 0.3 to 0.4

**Summary**: Workload is not admitted after upgrading from kueue 0.3 to 0.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/827

**Last updated**: 2023-06-06T13:17:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-01T18:24:21Z
- **Updated**: 2023-06-06T13:17:02Z
- **Closed**: 2023-06-06T13:17:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

**What happened**:

```
manager {"level":"error","ts":"2023-06-01T14:50:36.169498131Z","logger":"scheduler","caller":"scheduler/scheduler.go:306","msg":"Could not admit Workload and assign flavors in apiserver","workload":{"name":"job-jabba-job-y3tjgtaosbfc3aoctuqxtisu7bhw65edjy7eaoz5dvktyqo3qrhq-d9a73","namespace":"amp-batch"},"clusterQueue":{"name":"cluster-queue-part-mlops"},"error":"Workload.kueue.x-k8s.io \"job-jabba-job-y3tjgtaosbfc3aoctuqxtisu7bhw65edjy7eaoz5dvktyqo3qrhq-d9a73\" is invalid: status.admission.podSetAssignments.count: Required value","stacktrace":"sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).admit.func1\n\t/workspace/pkg/scheduler/scheduler.go:306\nsigs.k8s.io/kueue/pkg/util/routine.(*wrapper).Run.func1\n\t/workspace/pkg/util/routine/wrapper.go:44"}
```

**What you expected to happen**:

The admission to succeed.

**How to reproduce it (as minimally and precisely as possible)**:

This was reproduced by using the helm charts in the main branch, while using a 0.3.1 binary.

**Anything else we need to know?**:

We probably need to make `count` optional.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T18:24:33Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-06-01T19:01:25Z

@alculquicondor , this could, theoretically, only happen when the CRDs are v0.4 but the running manager is still 0.3 , do we want to cover this scenario? 

Anyway I'll have another look on Tuesday.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T19:05:32Z

In the case of admission, you are right. And no, we don't need to support that.

But I would be worried about cases where a 0.4 controller doesn't populate the field for an old workload, and gets rejected by the API. Although I'm not sure if this is possible. Maybe the controller would still send `count: 0`.

> Anyway I'll have another look on Tuesday.

Thanks!

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T05:46:05Z

It looks like there is  another way we can get to that error. While SSA even if only an unrelated condition is changed, the entire sub-resource is re validated. Well heed to make the count optional from an API point point view.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T13:11:03Z

Ah... yes, SSA does checks that other methods don't

Thanks for investigating!
