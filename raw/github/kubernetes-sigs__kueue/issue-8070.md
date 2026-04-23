# Issue #8070: Make race condition fails more descriptive

**Summary**: Make race condition fails more descriptive

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8070

**Last updated**: 2026-03-19T09:53:35Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-12-04T12:35:33Z
- **Updated**: 2026-03-19T09:53:35Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently, race condition errors look like this:

```
There were failures detected in the following suites:
  dra ./test/integration/singlecluster/controller/dra
```

This is very unclear and doesn’t show what’s actually happening.

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8063/pull-kueue-test-integration-baseline-main/1996549770306392064

**Why is this needed**:

To display the full trace for race conditions.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-04T12:35:40Z

/cc @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-04T12:57:47Z

@mszadkow Do we need the `--output-interceptor-mode=none` option? It looks like this option hides logs.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-04T13:45:55Z

It looks like the tests can get stuck without this flag if they hit a race condition:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8063/pull-kueue-test-integration-baseline-main/1996566523904266240

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-08T08:18:32Z

Yes, I don't remember exactly what was the reason to setup this flag, but I remember it was a trade-off.
It's either we see something went wrong or we stuck forever and we have no clue.
However I am all for it to enhance the message if possible.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:40:55Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:24Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:53:30Z

/remove-lifecycle stale
