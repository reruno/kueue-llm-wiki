# Issue #7693: AFS: entry penalties decay/are lost much faster than the config suggests

**Summary**: AFS: entry penalties decay/are lost much faster than the config suggests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7693

**Last updated**: 2025-11-26T14:12:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-17T09:17:14Z
- **Updated**: 2025-11-26T14:12:40Z
- **Closed**: 2025-11-26T14:12:40Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

**What happened**:

I have investigated logs of the flaky test https://github.com/kubernetes-sigs/kueue/issues/7688, and it seems the entry penalty for LQ was lost just after 62ms.

**What you expected to happen**:

Entry penalties to decay the same pace as regular usage.

**How to reproduce it (as minimally and precisely as possible)**:

The test flakes due to this.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:24:36Z

cc @PBundyra @IrvingMg

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T13:14:48Z

If the hypothesis in https://github.com/kubernetes-sigs/kueue/issues/7688#issuecomment-3541762979 is true then:
1. this is a production issue which can lead to admitting workloads bypassing the entry penalties
2. the issue is a race condition which is tricky to observe by users, and even if it happens then consequences are limited, which may explain why we haven't got this reported by users
3. we have a potential idea for fixing

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-18T08:00:13Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-18T18:34:02Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-11-19T14:18:51Z

Related issue: https://github.com/kubernetes-sigs/kueue/issues/6710
