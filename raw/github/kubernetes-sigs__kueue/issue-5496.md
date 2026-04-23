# Issue #5496: [flaky e2e test] TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Summary**: [flaky e2e test] TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5496

**Last updated**: 2025-12-01T10:49:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-04T09:26:41Z
- **Updated**: 2025-12-01T10:49:52Z
- **Closed**: 2025-12-01T10:49:51Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

/kind flake


**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5495/pull-kueue-test-e2e-tas-release-0-12/1930189621610680320

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/statefulset_test.go:75
  "level"=0 "msg"="Created namespace" "namespace"="e2e-tas-sts-zjpl4"
  STEP: Creating a StatefulSet @ 06/04/25 09:22:35.442
  STEP: Waiting for replicas to be ready @ 06/04/25 09:22:35.451
  STEP: ensure all pods are scheduled @ 06/04/25 09:22:41.28
  STEP: verify the assignment of pods are as expected with rank-based ordering @ 06/04/25 09:22:41.284
  [FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/statefulset_test.go:120 @ 06/04/25 09:22:41.287
  2025-06-04T09:22:41.627779295Z	INFO	KubeAPIWarningLogger	log/warning_handler.go:65	unknown field "spec.podSets[0].template.metadata.creationTimestamp"
• [FAILED] [8.284 seconds]
TopologyAwareScheduling for StatefulSet when Creating a StatefulSet [It] Should place pods based on the ranks-ordering
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/statefulset_test.go:75
  [FAILED] Expected object to be comparable, diff:   map[string]string{
  - 	"0": "kind-worker",
  + 	"0": "kind-worker5",
  - 	"1": "kind-worker2",
  + 	"1": "kind-worker6",
  - 	"2": "kind-worker3",
  + 	"2": "kind-worker7",
    }
  
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/statefulset_test.go:120 @ 06/04/25 09:22:41.287
------------------------------
[DeferCleanup (Suite)] 
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/suite_test.go:56
[DeferCleanup (Suite)] PASSED [0.000 seconds]
```
**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-04T09:26:52Z

cc @mbobrovskyi @mszadkow ptal

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-02T09:45:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T09:48:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-01T10:45:27Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T10:49:46Z

/close
we no longer have logs, and there have been many fixes to stability of the tests so maybe already resolved. If not resolved we anyway need to  wait for new occurrence to investigate, we will re-open then.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T10:49:52Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5496#issuecomment-3595868833):

>/close
>we no longer have logs, and there have been many fixes to stability of the tests so maybe already resolved. If not resolved we anyway need to  wait for new occurrence to investigate, we will re-open then.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
