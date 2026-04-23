# Issue #8780: [Dev mode] Trying to reuse a newly created cluster fails

**Summary**: [Dev mode] Trying to reuse a newly created cluster fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8780

**Last updated**: 2026-02-09T15:27:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-26T11:25:03Z
- **Updated**: 2026-02-09T15:27:26Z
- **Closed**: 2026-02-09T15:27:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 3

## Description


**What happened**:

I tried to run `E2E_MODE=dev make kind-image-build test-e2e` twice (with tests focused), but it fails on the second attempt.



**What you expected to happen**:

Re-run e2e tests on a cluster created by the previous run

**How to reproduce it (as minimally and precisely as possible)**:

1. Mark some test as focused using "FIt"
2. Run `E2E_MODE=dev make kind-image-build test-e2e` all good
3. Rerun `E2E_MODE=dev make kind-image-build test-e2e` fails with `error: SchemaError(sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadsSummary.items): unknown model in reference: "sigs.k8s.io~1kueue~1apis~1visibility~1v1beta1.PendingWorkload"`



**Anything else we need to know?**:

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/8093

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T11:25:16Z

cc @vladikkuzn @kshalot @mbobrovskyi  ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T11:29:51Z

/assign @vladikkuzn

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-29T17:00:42Z

This seems not only for development: https://github.com/kubernetes-sigs/kueue/issues/8873
