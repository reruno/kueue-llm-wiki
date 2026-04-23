# Issue #4760: Flaky e2e test:  Should run a RayCluster on worker if admitted

**Summary**: Flaky e2e test:  Should run a RayCluster on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4760

**Last updated**: 2025-03-24T09:36:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-24T06:15:07Z
- **Updated**: 2025-03-24T09:36:34Z
- **Closed**: 2025-03-24T09:36:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description


**What happened**:
Test failure: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-11/1903427712609947648

**What you expected to happen**:
no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
End To End MultiKueue Suite: kindest/node:v1.32.3: [It] MultiKueue when Creating a multikueue admission check Should run a RayCluster on worker if admitted expand_less	1m49s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:848 with:
Expected
    <int32>: 1
to equal
    <int32>: 0 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:848 with:
Expected
    <int32>: 1
to equal
    <int32>: 0
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:850 @ 03/22/25 13:07:40.254
}
```
This block in test in racy: https://github.com/kubernetes-sigs/kueue/blob/148043dece53fe857a6b13cf6836c11234394010/test/e2e/multikueue/e2e_test.go#L833-L851

And it is not related to the main purpose of the test. We decided to drop the analogous asserts for singlecluster in the PR: https://github.com/kubernetes-sigs/kueue/pull/4718#discussion_r2007473500

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T06:15:32Z

/kind flake
/assign @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-24T08:59:45Z

As discussed offline, modifying suspend that should be solely govern by Kueue itself, the test approach was wrong.
Removing this part.
