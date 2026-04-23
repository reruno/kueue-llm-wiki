# Issue #6033: Multikueue E2E_RUN_ONLY_ENV=true e2e test setup doesn't populate kubeconfig with context

**Summary**: Multikueue E2E_RUN_ONLY_ENV=true e2e test setup doesn't populate kubeconfig with context

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6033

**Last updated**: 2026-03-19T09:52:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-07-18T22:04:51Z
- **Updated**: 2026-03-19T09:52:02Z
- **Closed**: 2026-03-19T09:52:01Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
When I run: 
`make kind-image-build test-multikueue-e2e E2E_RUN_ONLY_ENV=true PLATFORMS=linux/arm64`

Then:
```
$ kind get clusters

kind-manager
kind-worker1
kind-worker2
```

Then I run: `kubectl config get-contexts`
 
The kubeconfigs do not show up for me to use. I have to manually run: `kind get kubeconfig --name kind-manager` to get the kubeconfig. 

**Why is this needed**:
I need to be able to run `make kind-image-build test-multikueue-e2e E2E_RUN_ONLY_ENV=true PLATFORMS=linux/arm64` to iterate on debugging quickly and see controller logs / observe cluster state while the kind cluster is still up and running. This means I want to be able to switch contexts quickly. 

For regular e2e tests, when I have the `E2E_RUN_ONLY_ENV=true` flag it automatically sets my kind context for me.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-18T22:05:04Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-16T23:22:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-16T00:21:11Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:46:35Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:47:17Z

I proposed some generic solution which would help here: https://github.com/kubernetes-sigs/kueue/issues/8093

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:26:16Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:19Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:51:55Z

/close
I think this is already done by https://github.com/kubernetes-sigs/kueue/issues/9063

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T09:52:02Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6033#issuecomment-4088977579):

>/close
>I think this is already done by https://github.com/kubernetes-sigs/kueue/issues/9063


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
