# Issue #67: Make unit tests run at least 3 times

**Summary**: Make unit tests run at least 3 times

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/67

**Last updated**: 2022-03-01T15:15:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T21:00:14Z
- **Updated**: 2022-03-01T15:15:49Z
- **Closed**: 2022-03-01T15:15:49Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@binacs](https://github.com/binacs)
- **Comments**: 1

## Description

We should not allow any flakiness in our unit tests. The prow job should run the tests with `-race -count 3`

Leave the option in the Makefile to run the tests only once (by default), as it's likely useful during development.

/priority important-soon
/kind cleanup

## Discussion

### Comment by [@binacs](https://github.com/binacs) — 2022-02-26T05:59:13Z

/assign
