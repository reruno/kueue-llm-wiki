# Issue #3600: [multiKueue flakes] Creating a multikueue admission check Should run a job on worker if admitted

**Summary**: [multiKueue flakes] Creating a multikueue admission check Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3600

**Last updated**: 2024-12-03T11:13:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-20T10:11:03Z
- **Updated**: 2024-12-03T11:13:41Z
- **Closed**: 2024-12-03T11:13:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

/kind flake

**What happened**:

The multikueue e2e test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3591/pull-kueue-test-multikueue-e2e-main/1859173059118764032

**What you expected to happen**:

To flakes

**How to reproduce it (as minimally and precisely as possible)**:

Run on CI

**Anything else we need to know?**:

```
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:229 with:
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:229 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:230 @ 11/20/24 10:02:46.412
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T10:11:13Z

cc @mszadkow @mbobrovskyi 
PTAL

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-11-21T10:51:32Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-02T15:18:06Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T11:13:01Z

/close 

Due to duplicate of https://github.com/kubernetes-sigs/kueue/issues/3581

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-03T11:13:07Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3600#issuecomment-2514252013):

>/close 
>
>Due to duplicate of https://github.com/kubernetes-sigs/kueue/issues/3600


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
