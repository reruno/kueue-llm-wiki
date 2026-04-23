# Issue #2115: [kueuectl] Add list LocalQueue command

**Summary**: [kueuectl] Add list LocalQueue command

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2115

**Last updated**: 2024-05-13T14:14:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-02T06:24:56Z
- **Updated**: 2024-05-13T14:14:49Z
- **Closed**: 2024-05-13T14:14:49Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add list LocalQueue command.

**Why is this needed**:
To get list LocalQueues that match the given criteria: point to a specific CQ, being active/inactive, belonging to the specified namespace or matching the label selector.

Design details https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#list-localqueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-02T06:44:13Z

@mbobrovskyi Could you track all commands by https://github.com/kubernetes-sigs/kueue/issues/2076?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-02T23:22:59Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-02T23:24:10Z

/assign @mbobrovskyi @vladikkuzn @IrvingMg @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-03T07:24:14Z

/unassign @mbobrovskyi @vladikkuzn @IrvingMg @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-03T17:38:43Z

/assign @mbobrovskyi
