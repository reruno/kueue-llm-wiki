# Issue #1112: Avoid capturing the tests *testing.T in subtests

**Summary**: Avoid capturing the tests *testing.T in subtests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1112

**Last updated**: 2023-09-18T15:51:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-09-12T05:47:26Z
- **Updated**: 2023-09-18T15:51:17Z
- **Closed**: 2023-09-18T14:24:32Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
https://github.com/kubernetes-sigs/kueue/pull/1079/files#r1322068774

**Why is this needed**:
Otherwise , a subtest failing will fail the parent test.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-18T14:08:12Z

/assign @trasc
