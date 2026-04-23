# Issue #6804: Follow-ups related to status.nodesToReplace

**Summary**: Follow-ups related to status.nodesToReplace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6804

**Last updated**: 2025-09-16T09:42:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-12T10:38:13Z
- **Updated**: 2025-09-16T09:42:14Z
- **Closed**: 2025-09-16T09:42:14Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Address the follow ups to https://github.com/kubernetes-sigs/kueue/pull/6648

In particular before the release the important is the comment affecting API: https://github.com/kubernetes-sigs/kueue/pull/6648#discussion_r2341231938

In conclusion, change nodesToReplace to unhealthyNodes with subfield "Name".

**Why is this needed**:

To make sure all comments are addressed.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T10:39:47Z

cc @tenzen-y @pajakd @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-12T10:56:34Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T08:10:22Z

@mbobrovskyi please also address https://github.com/kubernetes-sigs/kueue/pull/6648#discussion_r2341241428. I believe I addressed https://github.com/kubernetes-sigs/kueue/pull/6648#discussion_r2341236322 in the response.
