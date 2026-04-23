# Issue #2678: Overadmission after deleting resource from borrowing CQ

**Summary**: Overadmission after deleting resource from borrowing CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2678

**Last updated**: 2024-08-22T18:10:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-07-23T10:12:28Z
- **Updated**: 2024-08-22T18:10:08Z
- **Closed**: 2024-08-22T18:10:08Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

Consider the following scenario. We have two CQs in the same Cohort:
```
CQ1:
  1 CPU, 1 Memory
CQ2:
  2 CPU, 1 Memory
```

First, create WL1 in CQ1 which uses (2 CPU, 2 Memory)
Next, create WL2 in CQ2 which uses (1 CPU, 1 Memory). WL2 is initially suspended, as there is no available Memory.

Update the CQ definitions so that CQ1 no longer provides Memory
```
CQ1:
  1 CPU
CQ2:
  2 CPU, 1 Memory
```
WL2 admits, while WL1 is still running. We have admitted (3 CPU, 3 Memory), while the Cohort has total of (3 CPU, 1 Memory).

We filter out usage of no longer existing `FlavorResources` [here](https://github.com/kubernetes-sigs/kueue/blob/d6cbd8c77e9a37fd172452960bd7a87f89b3be47/pkg/cache/clusterqueue.go#L170-L171)

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-25T13:47:33Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-29T09:04:22Z

Just to clarify, the issue is about making sure no workloads get admitted in the scenario (WL2 does not get admitted). 

It is ok to let WL1 continue running. Eviction of over-committed workloads is out-of-scope of this issue. It could happen even when the capacity of a single CQ is reduced. We will handle / prioritize this independently.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-15T06:19:17Z

Is this a valid use case? Should we support this case? Or maybe we should prohibit user to do that on webhooks? 

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-15T13:08:04Z

No, reducing or removing resources from a CQ is a valid use case
