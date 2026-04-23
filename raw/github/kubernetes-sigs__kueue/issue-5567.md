# Issue #5567: Manage dependency versions list in a single place

**Summary**: Manage dependency versions list in a single place

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5567

**Last updated**: 2025-06-09T12:22:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-09T10:55:44Z
- **Updated**: 2025-06-09T12:22:31Z
- **Closed**: 2025-06-09T12:22:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Move all dependencies list of dependencies to the head of https://github.com/kubernetes-sigs/kueue/blob/ab9936ac3c2459e2b19fbebf1be7e26407bbb4bd/Makefile-deps.mk

**Why is this needed**:

Currently, we are managing Go project-related dependency versions in some places (Makefile-test.mk / Makefile-deps.mk). However, it would be better to manage those a single place to mitigate duplicated declarations in multiple places.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T10:56:02Z

cc @mbobrovskyi @mimowo

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-09T11:33:03Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T11:33:56Z

sgtm
