# Issue #334: Use ResourceFlavor.metadata.labels instead of ResourceFlavor.labels

**Summary**: Use ResourceFlavor.metadata.labels instead of ResourceFlavor.labels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/334

**Last updated**: 2022-08-25T18:04:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-16T14:04:08Z
- **Updated**: 2022-08-25T18:04:10Z
- **Closed**: 2022-08-25T18:04:10Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@thisisprasad](https://github.com/thisisprasad)
- **Comments**: 11

## Description

**What would you like to be cleaned**:

Since we are already thinking of v1beta2, we could consider deleting the field `.labels` and use `.metadata.labels` instead.

**Why is this needed**:

Users could be confused trying to use `.metadata.labels` which wouldn't give the results they want.

I can't think of a use case where a user would want to use `metadata.labels` without wanting them to match workloads' node selectors.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-16T14:04:22Z

@ahg-g thoughts?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-16T18:12:01Z

sgtm

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-16T18:45:07Z

The ResourceFlavor struct field `.labels` is currently being referred/used by:
1. `cache`
2. `Snapshot` unit tests
3. `Job controller`
4. `Scheduler` and its unit tests
5. resourceFlavor `webhook validation`

The changes to `resourceFlavor` struct would require changes in the above places.

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-16T18:45:34Z

I would like to work on this
/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-16T20:17:19Z

Thanks @thisisprasad

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-22T15:46:19Z

Any progress on this?

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-22T18:43:21Z

Working on the changes. Midway through. No blockers till now.

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-23T18:41:18Z

I think we should also update the documentation related to resourceFlavors as the `labels` field is repositioned. Changes would be required in `/docs/concepts/` and `/docs/tasks/` directories.

Will it be fine to update the documentation in the same PR as of cleanup code?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T19:05:34Z

Yes, that's fine and I would encourage it :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T14:33:52Z

Any progress? Since pretty much everything else is ready for 0.2.0 and this is low priority, we can leave it for 0.3.0

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-25T12:46:13Z

I've raised PR for this.

Apologies for the delay.
