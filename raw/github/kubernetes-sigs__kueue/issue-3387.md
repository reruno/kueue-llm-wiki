# Issue #3387: [kjobctl] Add support for `kueue.x-k8s.io/max-exec-time-seconds` in other modes.

**Summary**: [kjobctl] Add support for `kueue.x-k8s.io/max-exec-time-seconds` in other modes.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3387

**Last updated**: 2024-11-18T10:06:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-10-31T06:23:32Z
- **Updated**: 2024-11-18T10:06:54Z
- **Closed**: 2024-11-18T10:06:54Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
As follow up for https://github.com/kubernetes-sigs/kueue/pull/3321, add support for `kueue.x-k8s.io/max-exec-time-seconds` in other kjobctl modes.

**Why is this needed**:
We already support `kueue.x-k8s.io/max-exec-time-seconds` in kjobctl's Slurm mode. It would be great to apply the same logic to other modes as well.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-05T15:30:17Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-05T15:58:44Z

We have `--time` flag for Slurm mode with very specific formats ("minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds"). But I'm not sure that it is good to use in another kjob modes.

@mimowo @mwysokin Should we create separate flag (e.g. --max-exec-time) with seconds or duration format? Or it's better to keep current and use for other modes the same format? WDYT?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-12T12:45:27Z

Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-13T07:54:37Z

IIUC all other modes (can you list?) also support the same semantics of accounting for the max-exec-time? So, I think it could be a bit confusing to name the param differently. Also, the slurm format seems sensible, so I see no problem with reusing.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-13T08:11:20Z

> can you list?

Job, Interactive (Pod), Rayjob, Raycluster, Slurm
