# Issue #8585: MultiKueue: workloads from worker clusters are deleted prematurely

**Summary**: MultiKueue: workloads from worker clusters are deleted prematurely

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8585

**Last updated**: 2026-01-15T08:07:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-14T12:08:47Z
- **Updated**: 2026-01-15T08:07:38Z
- **Closed**: 2026-01-15T08:07:37Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 9

## Description

**What happened**:

NOTE: this is based on static code analysis for now, specifically of this code: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/multikueue/workload.go#L409-L420

This is quite important for the use-case of searching for capacity with ProvisioningRequests. Otherwise the we only run one ProvisiniongRequest at the time.

**What you expected to happen**:

Deletion of the other workers should be deferred only after one is admitted.

**Anything else we need to know?**:

Since this issue existed for long we should introduce a feature gate for safety.

I consider it a bug, becuase it was stated in the [KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/693-multikueue#proposal) that we should wait until the workload is admitted, rather than quota reserving, sepecifically:

If a remote workload is **admitted** first, the job will be created in the remote cluster with a kueue.x-k8s.io/prebuilt-workload-name label pointing to that clone. Then it will remove the workloads from the remaining worker clusters and allow the single instance of the job to proceed. The workload will be also admitted in the management cluster.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T12:11:47Z

/assign @mbobrovskyi 
tentatively
cc @mszadkow @olekzabl @mwielgus @yaroslava-serdiuk

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-14T13:16:21Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-14T13:20:10Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:30:27Z

/priority important-soon

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-14T14:20:38Z

Should this feature be in Alpha stage?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T14:22:25Z

I think this is a bug. IIUC the current implementation is inconsistent with the KEP, and I don't see a need for new API. Let me know if I'm missing something.

Since this behavior was for long we can use a feature gate for safety.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T14:38:44Z

Using Admitted rather than QuotaReserved should not have a difference for clusters which are not using custom admission checks.  

However, the current behavior of looking into QuotaReserved is currently broken when using provisioning requests, because we prefer to look for the capacity at the same time on all clusters, still first one wins. If one can limit the number of clusters to be checked in parallel, they can use the status.nominatedClusterNames.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-14T14:51:45Z

I think the question for Alpha was in regards to the feature gate. 

IIUC, we need to add a new feature gate, e.g.`MultiKueueWaitForWorkloadAdmitted`, which changes the condition to check from QuotaReserved to Admitted before cleaning up non-selected worker workloads. Should this start as Alpha?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T14:53:11Z

I see, but I  think with Beta, unless the. implementation proves to be very complex and risky
