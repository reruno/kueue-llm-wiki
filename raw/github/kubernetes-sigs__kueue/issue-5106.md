# Issue #5106: [Flaky test] Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeou

**Summary**: [Flaky test] Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeou

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5106

**Last updated**: 2025-12-10T16:17:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-24T18:29:03Z
- **Updated**: 2025-12-10T16:17:36Z
- **Closed**: 2025-12-10T16:17:36Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 11

## Description

**What happened**:

failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5059/pull-kueue-test-e2e-customconfigs-main/1915465994071969792

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```

End To End Custom Configs handling Suite: kindest/node:v1.32.3: [It] WaitForPodsReady Job Controller E2E when WaitForPodsReady has default Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeout expand_less	1m16s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/waitforpodsready_test.go:207 with:
Expected
    <*v1beta1.RequeueState | 0x0>: nil
not to be nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/waitforpodsready_test.go:207 with:
Expected
    <*v1beta1.RequeueState | 0x0>: nil
not to be nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/waitforpodsready_test.go:221 @ 04/24/25 18:13:11.195
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T18:29:10Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T18:29:31Z

cc @PBundyra @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-29T08:49:56Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-19T14:16:46Z

Unfortunately, we missed the logs from `kueue-controller-manager`. This was already fixed in #5164. It would be great to catch one more failure and check the logs from `kueue-controller-manager`.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-19T14:22:38Z

Currently, the only possibility I see is that there's just enough time for the Pod to be rerun due to a tiny timeout.

https://github.com/kubernetes-sigs/kueue/blob/10fea3f1850bc2e88966668e36a4390af37e2565/test/e2e/customconfigs/waitforpodsready_test.go#L212

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-17T14:48:41Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:49:51Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T03:37:23Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8063/pull-kueue-test-e2e-customconfigs-main/1996583380052873216.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T12:00:12Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8068/pull-kueue-test-e2e-customconfigs-main/1996555317856440320

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T16:45:12Z

/unassign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-05T21:28:30Z

/assign @sohankunkerkar
