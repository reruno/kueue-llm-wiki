# Issue #7193: [pull-kueue-test-unit-main] flakes

**Summary**: [pull-kueue-test-unit-main] flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7193

**Last updated**: 2026-04-18T13:17:56Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-07T13:21:14Z
- **Updated**: 2026-04-18T13:17:56Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 3

## Description

/kind flake

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7192/pull-kueue-test-unit-main/1975548359393415168

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:


```
✓  pkg/visibility/api/v1beta1 (4.917s) (coverage: 1.7% of statements in ./...)
✓  pkg/workload (5.104s) (coverage: 3.4% of statements in ./...)
✓  pkg/workloadslicing (5.128s) (coverage: 1.7% of statements in ./...)
✓  pkg/scheduler (1m27.613s) (coverage: 18.6% of statements in ./...)
=== Errors
go tool covdata: fork/exec /root/.cache/go-build/c1/c1707552bde119e88452d113c7246675a793dfb74fec88738715040232b0eab9-d/covdata: text file busy
DONE 9666 tests, 1 error in 270.700s
make: *** [Makefile-test.mk:68: test] Error 1
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:47:06Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T12:48:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T13:17:52Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
