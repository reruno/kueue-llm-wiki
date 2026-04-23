# Issue #6922: TEST_LOG_LEVEL inconsistent

**Summary**: TEST_LOG_LEVEL inconsistent

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6922

**Last updated**: 2025-10-03T07:40:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-09-19T09:09:28Z
- **Updated**: 2025-10-03T07:40:58Z
- **Closed**: 2025-10-03T07:40:58Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

**What would you like to be cleaned**:
Regarding [TEST_LOG_LEVEL](https://kueue.sigs.k8s.io/docs/contribution_guidelines/testing/#increase-logging-verbosity)

The current behavior is the following:

- `go test` higher value = more verbosity
- `make test` doesn't change
- `make test-integration` lower value = more verbosity

- [ ] Make this behavior consistent
- [ ] Ensure documentation is consistent

**Why is this needed**:

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-01T20:18:51Z

/assign
