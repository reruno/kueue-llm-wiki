# Issue #3741: MultiKueue tests fail on the release branches

**Summary**: MultiKueue tests fail on the release branches

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3741

**Last updated**: 2024-12-05T15:05:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-05T08:47:37Z
- **Updated**: 2024-12-05T15:05:19Z
- **Closed**: 2024-12-05T15:05:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 12

## Description

**What happened**:

The e2e tests for MultiKueue fail on the release branches: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-e2e-release-0-9, and https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-e2e-release-0-8

**What you expected to happen**:

No failures on the release branches

**How to reproduce it (as minimally and precisely as possible)**:

CI

**Anything else we need to know?**:

The release-blocking tests have been recently added.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T08:47:54Z

/assign @mbobrovskyi 
cc @kannon92

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T09:55:08Z

@IrvingMg is https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-multikueue-e2e-release-0-9/1864585975066267648 related to https://github.com/kubernetes-sigs/kueue/issues/3664?

UPDATED: Yeah, looks like the same issue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T10:22:35Z

@mszadkow PTAL https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-multikueue-e2e-release-0-8/1864585975003353088

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T10:25:30Z

is this already fixed with https://github.com/kubernetes-sigs/kueue/pull/3743 and https://github.com/kubernetes-sigs/kueue/pull/3742? I so, then we can close

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T10:25:51Z

I think https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-multikueue-e2e-release-0-8/1864585975003353088 another issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T10:32:33Z

ok, please investigate then

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T12:21:41Z

OK. This test on release-0.8 branch is not working with 1.31.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T12:35:13Z

The JobManagedBy was disabled on 1.31, so we have two choices: enable it in the kind config, and enable `MultiKueueBatchJobWithManagedBy`. Or keep it disabled, and also disable `MultiKueueBatchJobWithManagedBy`. These features (in k8s and kueue) need to be enabled in sync basically.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T12:36:15Z

but if there is no quick fix I don't think we need to worry too much, once we release 0.10 we can drop that testing suite I believe, we are not planning to release 0.8.5 (I hope) cc @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T15:03:12Z

@mbobrovskyi  are we now done after https://github.com/kubernetes-sigs/kueue/pull/3745?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T15:05:12Z

/close

Due to https://github.com/kubernetes-sigs/kueue/pull/3745 merged.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-05T15:05:17Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3741#issuecomment-2520570235):

>/close
>
>Due to https://github.com/kubernetes-sigs/kueue/pull/3745 merged.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
