# Issue #1038: Update workload when job changes before admission

**Summary**: Update workload when job changes before admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1038

**Last updated**: 2023-10-31T16:38:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GhangZh](https://github.com/GhangZh)
- **Created**: 2023-08-03T12:55:28Z
- **Updated**: 2023-10-31T16:38:47Z
- **Closed**: 2023-10-31T16:38:47Z
- **Labels**: `kind/feature`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 6

## Description

The current workload design is that if the configuration of workload and job is found to be inconsistent, the current workload will be deleted and re-created.

If there are some special scenarios where I need to change the job configuration, it will cause my job to be re-queued, which is not very reasonable from a product perspective, the expectation is that the workload will not be re-created but will change as the job changes.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-03T14:54:58Z

Do you mean you would like to change the job while it's queued (suspended) or at any point?

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-08-04T02:40:06Z

> 
Yes, I'll modify it when the job is queued or suspended

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-04T12:06:31Z

That sounds feasible.

@trasc, could you investigate if it's possible?

### Comment by [@trasc](https://github.com/trasc) — 2023-08-04T12:18:34Z

Yes, it should be doable.
/assign

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-10-03T13:52:35Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-03T14:28:05Z

/unassign @trasc
