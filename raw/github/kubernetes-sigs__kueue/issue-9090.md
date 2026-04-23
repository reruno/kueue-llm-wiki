# Issue #9090: Add logs and metrics around API conversion webhooks

**Summary**: Add logs and metrics around API conversion webhooks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9090

**Last updated**: 2026-02-11T08:36:22Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-02-10T12:00:25Z
- **Updated**: 2026-02-11T08:36:22Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**:

Add metrics and logs in conversion webhooks.

**Why is this needed**:

At this moment there is no visibility into how much conversions are going on, leading to issues with troubleshooting Kueue on large clusters. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T13:03:46Z

It might be that controller-runtime is already logging the received conversion webhook requests, just on a deep logging level. Maybe it also has some metrics which we could surface / document better instead of adding new. I'm not sure, but worth investigating what is already in controller-runtime wrt conversion webhooks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T08:36:22Z

If we want to fully handle conversion loggings, we need to stop relying on auto-generation. Fully scratch conversion webhook could control everything, but implementation and maintaining costs will be huge...
