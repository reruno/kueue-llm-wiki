# Issue #2039: Fix logging of the workload status when using admission checks

**Summary**: Fix logging of the workload status when using admission checks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2039

**Last updated**: 2024-06-12T16:05:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-23T08:39:02Z
- **Updated**: 2024-06-12T16:05:14Z
- **Closed**: 2024-06-12T16:05:12Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

When ProvReq admission check is used, and it is in the QuotaReserved state, then the workload controller logs that it is already admitted, which is misleading. 

The produced logs look similar to:
```
{"caller":"core/workload_controller.go:507", "clusterQueue":"dws-cluster-queue", "level":"Level(-2)", "logger":"workload-reconciler", "msg":"Workload update event", "prevStatus":"pending", "queue":"dws-local-queue", "status":"admitted", "workload":{…}}
```

**What you expected to happen**:

Log properly when the workload is in the QuotaReserved, and when in the Admitted status.

**How to reproduce it (as minimally and precisely as possible)**:

Create a workload with a ProvReq and check the logs when the workload is waiting for provisioning of the request.

**Anything else we need to know?**:

Here is the code: https://github.com/kubernetes-sigs/kueue/blob/92baacd06e54f57de85a15590a1780eb84455941/pkg/controller/core/workload_controller.go#L677-L679.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-23T08:39:11Z

/cc @alculquicondor

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-12T15:56:53Z

@mimowo Looks like it's already fixed.

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go#L69-L74

```
{"workload": {"name":"wl","namespace":"provisioning-5v2pn"}, "queue": "queue", "status": "quotaReserved", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-12T16:04:59Z

You are correct. We can close it

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-12T16:05:08Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-12T16:05:13Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2039#issuecomment-2163416780):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
