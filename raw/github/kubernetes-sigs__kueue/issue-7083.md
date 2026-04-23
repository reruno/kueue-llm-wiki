# Issue #7083: Increase CPU requests for the pull-kueue-verify and pull-kueue-test-unit Jobs

**Summary**: Increase CPU requests for the pull-kueue-verify and pull-kueue-test-unit Jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7083

**Last updated**: 2025-10-01T12:20:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-30T13:59:40Z
- **Updated**: 2025-10-01T12:20:24Z
- **Closed**: 2025-10-01T12:20:24Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to increase CPU requests for pull-kueue-verify and pull-kueue-test-unit to improve CI performance.

**Why is this needed**:

As I show in the following images, the pull-kueue-verify Job is too slow due to CPU pressure:

https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-1h&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-verify-main&var-build=All&refresh=30s

<img width="2208" height="672" alt="Image" src="https://github.com/user-attachments/assets/03b8a2eb-2027-4f5a-8c78-c772e496f439" />
<img width="2238" height="718" alt="Image" src="https://github.com/user-attachments/assets/b2eee5ac-f0c1-408a-a30d-1adc6562377d" />

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T13:59:50Z

cc @mimowo @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:01:09Z

+1. I think it is justified to bump to 6 seeing the graphs

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T14:02:25Z

For pull-kueue-test-unit, I observed the same situations:

https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-1h&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-unit-main&var-build=All&refresh=30s

<img width="1060" height="766" alt="Image" src="https://github.com/user-attachments/assets/8cd06809-2f6f-4237-a147-9593a44d8d88" />
<img width="606" height="758" alt="Image" src="https://github.com/user-attachments/assets/1d7fd6d2-ceee-496c-90a3-f5b20555abe4" />
<img width="708" height="790" alt="Image" src="https://github.com/user-attachments/assets/6e5b3be1-f7c9-4a23-a02e-c67985fa1932" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:08:06Z

Here I would bump to 4.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T14:09:54Z

> +1. I think it is justified to bump to 6 seeing the graphs

> Here I would bump to 4.

SGTM

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-30T15:57:06Z

Done in https://github.com/kubernetes/test-infra/pull/35615

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T04:16:00Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-01T04:16:05Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7083#issuecomment-3354681428):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T04:18:33Z

We can still see the CPU throttling in the following.
So, I would propose increasing it to 6 Cores for pull-kueue-unit, and to 8 Cores for pull-kueue-verify.

cc @mimowo 

- pull-kueue-verify

<img width="2212" height="710" alt="Image" src="https://github.com/user-attachments/assets/f232c4cb-1cef-4be0-a899-7eecfc21ce3d" />
<img width="1570" height="776" alt="Image" src="https://github.com/user-attachments/assets/66de1bb4-41d3-4bac-aaef-50d953ff5947" />

- pull-kueue-unit

<img width="1340" height="698" alt="Image" src="https://github.com/user-attachments/assets/18985677-4cdf-4db9-b565-ff79cf4ac897" />
<img width="2156" height="700" alt="Image" src="https://github.com/user-attachments/assets/13503739-8c17-4642-8bb7-8177a01373e4" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T05:22:18Z

sgtm

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-01T09:51:17Z

/assign
