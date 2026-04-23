# Issue #4480: Flaky e2e test:  StatefulSet integration when StatefulSet created should admit group that fits

**Summary**: Flaky e2e test:  StatefulSet integration when StatefulSet created should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4480

**Last updated**: 2025-03-19T08:14:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-04T18:09:02Z
- **Updated**: 2025-03-19T08:14:01Z
- **Closed**: 2025-03-19T08:14:00Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

e2e failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4341/pull-kueue-test-e2e-main-1-31/1896970322809196544

**What you expected to happen**:

no random failures

**How to reproduce it (as minimally and precisely as possible)**:

run ci

**Anything else we need to know?**:

Actually 3 tests failed, which might be related:

```
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should admit group that fits expand_less	1m8s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:133 @ 03/04/25 17:19:52.185
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-singlecluster-1.31.0%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F4341%2Fpull-kueue-test-e2e-main-1-31%2F1896970322809196544%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4341/pull-kueue-test-e2e-main-1-31/1896970322809196544&lensIndex=2#)
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should allow to update the PodTemplate in StatefulSet expand_less	1m7s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:180 with:
Expected
    <string>: "...t:2.52@sha2..."
to equal               |
    <string>: "...t:2.53@sha2..." failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:180 with:
Expected
    <string>: "...t:2.52@sha2..."
to equal               |
    <string>: "...t:2.53@sha2..."
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:182 @ 03/04/25 17:20:59.406
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-singlecluster-1.31.0%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F4341%2Fpull-kueue-test-e2e-main-1-31%2F1896970322809196544%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4341/pull-kueue-test-e2e-main-1-31/1896970322809196544&lensIndex=2#)
End To End Suite: kindest/node:v1.31.0: [It] StatefulSet integration when StatefulSet created should delete all pods on scale down to zero expand_less	1m1s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:233 with:
Expected
    <int32>: 2
to equal
    <int32>: 0 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:233 with:
Expected
    <int32>: 2
to equal
    <int32>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:234 @ 03/04/25 17:22:00.465
}
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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-04T18:10:25Z

cc @mbobrovskyi @mszadkow @nasedil

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-04T18:17:48Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T11:59:15Z

Another occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4503/pull-kueue-test-e2e-main-1-30/1897973595200557056

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:13:55Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:14:00Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4480#issuecomment-2735678150):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
