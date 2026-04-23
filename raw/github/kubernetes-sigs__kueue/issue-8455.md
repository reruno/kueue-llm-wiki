# Issue #8455: Deprecate use of wl as short name for Kueue Workload

**Summary**: Deprecate use of wl as short name for Kueue Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8455

**Last updated**: 2026-01-08T17:07:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-01-07T16:22:33Z
- **Updated**: 2026-01-08T17:07:41Z
- **Closed**: 2026-01-08T17:07:41Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 7

## Description

ref: https://github.com/kubernetes-sigs/kueue/issues/8113

We will need to deprecate use of "wl" as shortName for 0.16.

Another item we should take is to use stable short names (kubectl get kueueworkload) instead of kueue get workload.

With pending inclusion of workload object in tree we will hit issues in our documentation once Kueue workload is enabled.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-07T16:23:05Z

@mimowo @tenzen-y 

For "deprecation" do we remove this in 0.16? Or just add a release note?

I don't really know how to deprecate a shortname honestly.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-07T16:26:17Z

TBH, I think that we can remove "wl" altogether.
But, let me know if @mimowo and @kannon92 want to keep "wl" during a few Kueue minor releases.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T03:54:21Z

/kind feature

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T07:30:33Z

/priority important-soon

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T07:32:32Z

> TBH, I think that we can remove "wl" altogether.
> But, let me know if @mimowo and @kannon92 want to keep "wl" during a few Kueue minor releases.

WDYT about cherrypicking the new short names, but drop the "wl" in 0.16+. So 0.14.x and 0.15.x will continue to support "wl".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T14:02:23Z

> > TBH, I think that we can remove "wl" altogether.
> > But, let me know if [@mimowo](https://github.com/mimowo) and [@kannon92](https://github.com/kannon92) want to keep "wl" during a few Kueue minor releases.
> 
> WDYT about cherrypicking the new short names, but drop the "wl" in 0.16+. So 0.14.x and 0.15.x will continue to support "wl".

That sounds good to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T14:20:53Z

@kannon92 could you prepare the PR to drop "wl" for 0.16+?
