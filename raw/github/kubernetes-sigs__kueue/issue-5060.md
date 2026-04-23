# Issue #5060: Migrate from tools package to Go tool directive

**Summary**: Migrate from tools package to Go tool directive

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5060

**Last updated**: 2025-06-05T05:04:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-21T19:58:10Z
- **Updated**: 2025-06-05T05:04:40Z
- **Closed**: 2025-06-05T05:04:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We would like to migrate from the tools package to the tool directive for tools version management.

- The current tools package: https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/hack/internal/tools/pinversion.go

- new tool directive: https://tip.golang.org/doc/modules/managing-dependencies#tools

**Why is this needed**:

Since v1.24, Go introduced a new tool version management mechanism called the tool directive.
So, It would be better to migrate to it.

## Discussion

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-04-22T08:08:46Z

/assign
I can take care of this one 😊
