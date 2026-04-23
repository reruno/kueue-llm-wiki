# Issue #30: Add scheduler integration tests

**Summary**: Add scheduler integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/30

**Last updated**: 2022-02-22T01:23:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-18T17:59:18Z
- **Updated**: 2022-02-22T01:23:46Z
- **Closed**: 2022-02-22T01:23:46Z
- **Labels**: `priority/important-soon`, `kind/test`
- **Assignees**: _none_
- **Comments**: 0

## Description

We have one that covers the job-controller on its own, we need a test that cover all other controllers together that includes creating queue, capacity and multiple jobs, and inspect that jobs are started as expected.
