# Issue #8321: Removing priority class is disallowed even for suspended workloads

**Summary**: Removing priority class is disallowed even for suspended workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8321

**Last updated**: 2025-12-18T16:23:25Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-12-18T10:58:33Z
- **Updated**: 2025-12-18T16:23:25Z
- **Closed**: 2025-12-18T15:14:49Z
- **Labels**: `kind/bug`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 5

## Description

Kueue version: 0.15.0

Currently, priority class labels for workloads can be:

* _changed_ (from non-empty to another non-empty) - for any workloads
* _added_ (from empty to non-empty) - for suspended workloads
  (TBH I don't know why such restriction - but for now I'd assume it's intended)
* _removed_ (from non-empty to empty) - **never**
  (which I guess is not intended, and should work analogous as adding).

This is due to this validation logic:

https://github.com/kubernetes-sigs/kueue/blob/b29f1b3a14194b70681524d9cc0a6ca2b3dfc86e/pkg/controller/jobframework/validation.go#L168-L170

`&&` and `||` have equal precedence, left binding, so the key expression parses as

```
(!isSuspended && IsWorkloadPriorityClassNameEmpty(oldObj)) || IsWorkloadPriorityClassNameEmpty(newObj)
```

while I guess the intended (and symmetric) behavior would be

```
!isSuspended && (IsWorkloadPriorityClassNameEmpty(oldObj) || IsWorkloadPriorityClassNameEmpty(newObj))
```

which would require explicit parentheses.

Real repro: see [this script](https://github.com/olekzabl/kueue/blob/repro-8321/hack/bug-repro/remove-wpc.sh) (and its [output](https://github.com/olekzabl/kueue/blob/repro-8321/hack/bug-repro/remove-wpc.out.txt)).

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-12-18T13:33:24Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-12-18T15:12:26Z

Ohh, I realized this is intended behavior, introduced in #5241.

Then, the only action here is to make code a bit less confusing. I'll make the current parenthesing explicit.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T15:14:08Z

And it would be good to include unit test or integration, so that we don't need to wait until e2e testing level to realize that.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-12-18T15:16:14Z

> And it would be good to include unit test or integration, so that we don't need to wait until e2e testing level to realize that.

Unit tests for this already existed.
TBH I just assumed they were "current-implementation-driven", my bad.
Only seeing an e2e test specifically for this raised an alert for me that it may be intended.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-12-18T15:53:24Z

Another thing I'd like to improve is the error message. Currently it says `field is immutable` which is false, and confusing.

See #8334 for the fix.
