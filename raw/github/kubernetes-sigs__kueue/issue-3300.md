# Issue #3300: Ensure the err is surfaced in e2e/integration tests to improve debuggability

**Summary**: Ensure the err is surfaced in e2e/integration tests to improve debuggability

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3300

**Last updated**: 2024-10-29T17:28:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-24T08:44:51Z
- **Updated**: 2024-10-29T17:28:57Z
- **Closed**: 2024-10-29T17:28:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

We use this pattern in many places :

```golang
if err := k8sClient.Get(ctx, wlLookupKey, createdWorkload); err != nil {
return false
}
```

We prefer to replace it with something like:
```golang
gomega.Eventually(func(g gomega.Gomega) {
	g.Expect(k8sClient.Get(ctx, wlLookupKey, createdWorkload)).Should(gomega.Succeed())
	...
}, util.LongTimeout, util.Interval).Should(gomega.Succeed())
```

This is a follow up to the discussion here: https://github.com/kubernetes-sigs/kueue/pull/3284#discussion_r1814544537

**Why is this needed**:

To improve debuggability.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-24T14:49:52Z

/assign

I already started working on it before.
