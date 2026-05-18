# Issue #9248: [FlakyTFJob controller with TopologyAwareScheduling should admit workload which fits in a required topology domain [Redundant]]

**Summary**: [FlakyTFJob controller with TopologyAwareScheduling should admit workload which fits in a required topology domain [Redundant]]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9248

**Last updated**: 2026-05-11T07:28:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-15T05:23:26Z
- **Updated**: 2026-05-11T07:28:46Z
- **Closed**: 2026-05-11T07:28:45Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

TFJob Controller Suite: [It] TFJob controller with TopologyAwareScheduling should admit workload which fits in a required topology domain [Redundant] 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9247/pull-kueue-test-integration-extended-release-0-15/2022899914614247424

**Failure message or logs**:
```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:1121 with:
Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type Active and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:1121 with:
Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type Active and status True
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/tfjob/tfjob_controller_test.go:353 @ 02/15/26 05:21:19.666
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T07:28:40Z

/close
Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-11T07:28:46Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9248#issuecomment-4418431536):

>/close
>Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
