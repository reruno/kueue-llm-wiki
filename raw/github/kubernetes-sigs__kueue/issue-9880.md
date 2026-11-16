# Issue #9880: Eliminate `ginkgo.Ordered` for singlecluster integration tests

**Summary**: Eliminate `ginkgo.Ordered` for singlecluster integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9880

**Last updated**: 2026-11-04T14:43:58Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-16T08:38:54Z
- **Updated**: 2026-11-04T14:43:58Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@unaimeds](https://github.com/unaimeds), [@Paramesh324](https://github.com/Paramesh324)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to eliminate ginkgo.Ordered for all integration tests, similarly as recently done for fair sharing tests.

Examples:
- https://github.com/kubernetes-sigs/kueue/blob/baf8a94160fe65077c17a1387c57055c6309ac01/test/integration/singlecluster/controller/core/clusterqueue_controller_test.go#L1151
- https://github.com/kubernetes-sigs/kueue/blob/baf8a94160fe65077c17a1387c57055c6309ac01/test/integration/singlecluster/webhook/core/localqueue_test.go#L33

**Why is this needed**:

This allows better parallelism for running tests, and thus shorter overall running time as we execute them all multiple threads.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T08:39:01Z

cc @mbobrovskyi

### Comment by [@Paramesh324](https://github.com/Paramesh324) — 2026-03-18T07:00:42Z

@mimowo Can i work on this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-18T07:02:13Z

Sure

### Comment by [@Paramesh324](https://github.com/Paramesh324) — 2026-03-18T07:06:38Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-14T09:29:15Z

@Paramesh324 @mbobrovskyi let me know what is the status here, I'm wondering if the big PR is a good approach, maybe we could iterate faster if this work is split into smaller chunks which we can approve faster, wdyt?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-07-13T10:00:34Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-07-13T10:16:31Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-10-22T18:18:25Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-10-23T07:31:20Z

/remove-lifecycle stale

### Comment by [@unaimeds](https://github.com/unaimeds) — 2026-11-04T14:43:58Z

/assign
