# Issue #9881: Eliminate ginkgo.Ordered for singlecluster e2e tests

**Summary**: Eliminate ginkgo.Ordered for singlecluster e2e tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9881

**Last updated**: 2026-04-06T05:23:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-16T08:40:12Z
- **Updated**: 2026-04-06T05:23:30Z
- **Closed**: 2026-04-06T05:23:30Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vamsikrishna-siddu](https://github.com/vamsikrishna-siddu)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to run all e2e tests in parallel, and to achieve we need to drop ginkgo.Ordered

Example: https://github.com/kubernetes-sigs/kueue/blob/baf8a94160fe65077c17a1387c57055c6309ac01/test/e2e/singlecluster/fair_sharing_test.go#L33

https://github.com/kubernetes-sigs/kueue/blob/baf8a94160fe65077c17a1387c57055c6309ac01/test/e2e/singlecluster/kueuectl_test.go#L32

**Why is this needed**:

For better parallelism and thus performance of running the tests.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T08:40:19Z

cc @mbobrovskyi

### Comment by [@vamsikrishna-siddu](https://github.com/vamsikrishna-siddu) — 2026-03-16T12:36:49Z

Hi @mimowo can i work on this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T12:45:40Z

sure

### Comment by [@vamsikrishna-siddu](https://github.com/vamsikrishna-siddu) — 2026-03-16T13:08:51Z

/assign
