# Issue #3343: Replace Background and TODO contexts with utiltesting.ContextWithLog in tests

**Summary**: Replace Background and TODO contexts with utiltesting.ContextWithLog in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3343

**Last updated**: 2024-10-29T18:02:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-28T12:41:27Z
- **Updated**: 2024-10-29T18:02:57Z
- **Closed**: 2024-10-29T18:02:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

We use TODO and Background context even though we create the local ctx with ContextWithLog. Example:
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/clusterqueue_test.go#L372-L384

**Why is this needed**:

To use consistent style. In some scenarios using Background context can result in leaking goroutines.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-28T12:41:34Z

/cc @mbobrovskyi @tenzen-y

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-29T08:30:27Z

/assign
