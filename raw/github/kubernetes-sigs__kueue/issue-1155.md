# Issue #1155: [Ray] Update Go Module version

**Summary**: [Ray] Update Go Module version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1155

**Last updated**: 2023-10-20T10:55:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-09-22T23:16:55Z
- **Updated**: 2023-10-20T10:55:40Z
- **Closed**: 2023-10-20T10:55:40Z
- **Labels**: `kind/feature`
- **Assignees**: [@lowang-bh](https://github.com/lowang-bh)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We should upgrade go module version for kuberay.

**Why is this needed**:
Our version is outdated. However, the dependabot could not update the version.

https://github.com/kubernetes-sigs/kueue/blob/f9273bef71e136c0eed659ae19fce178512a6f6a/go.mod#L16
https://github.com/ray-project/kuberay/releases/tag/v0.6.0

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-22T23:17:25Z

@trasc Could you take this one?

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-09-23T13:40:11Z

Hi @tenzen-y  Could I take it?

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-25T07:39:26Z

> Hi @tenzen-y Could I take it?
> 
> /assign

Sure.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-18T06:31:49Z

@lowang-bh are you still working on this?

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-10-20T07:09:48Z

> @lowang-bh are you still working on this?

Done in PR #1231
