# Issue #543: Reduce error outputs in integration tests

**Summary**: Reduce error outputs in integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/543

**Last updated**: 2023-05-15T10:07:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-02-02T06:14:21Z
- **Updated**: 2023-05-15T10:07:27Z
- **Closed**: 2023-05-15T10:07:26Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

When running `make test-integration`, we see lots of errors, some are because of the log framework like `log.Error()`, I didn't dig into that right now. 
```
  2023-02-02T14:05:05.797+08:00	ERROR	controller-runtime.certwatcher	certwatcher/certwatcher.go:147	error re-watching file	{"error": "lstat /var/folders/c_/7mkl6xtj6qz3dpn1ggg4d2yw0000gn/T/envtest-serving-certs-4223195164/tls.key: no such file or directory"}

...

  2023-02-02T14:04:59.887531+08:00	ERROR	controller-runtime.source	source/source.go:144	failed to get informer from cache
 ```

**Why is this needed**:

Avoid noice and maybe some potential bug there.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-02T06:14:48Z

/priority important-longterm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-02T13:19:16Z

Should we report this in controller-runtime instead?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-03T11:03:18Z

> Should we report this in controller-runtime instead?

If I confirmed this is the debt of controller-runtime 🙃

Firstly, do you think we should disable debug mode in testing? Only enable when needed like local development
```
2023-02-03T18:28:14.694468+08:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/mutate-kueue-x-k8s-io-v1alpha2-workload", "UID": "201ae153-0154-48d4-8b3d-955ee4b67237", "kind": "kueue.x-k8s.io/v1alpha2, Kind=Workload", "resource": {"group":"kueue.x-k8s.io","version":"v1alpha2","resource":"workloads"}}
  2023-02-03T18:28:14.69464+08:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/mutate-kueue-x-k8s-io-v1alpha2-workload", "code": 200, "reason": "", "UID": "201ae153-0154-48d4-8b3d-955ee4b67237", "allowed": true}
  2023-02-03T18:28:14.953776+08:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/mutate-kueue-x-k8s-io-v1alpha2-workload", "UID": "2e695058-f75d-46a6-9675-224a4b9413fc", "kind": "kueue.x-k8s.io/v1alpha2, Kind=Workload", "resource": {"group":"kueue.x-k8s.io","version":"v1alpha2","resource":"workloads"}}
  2023-02-03T18:28:14.954006+08:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/mutate-kueue-x-k8s-io-v1alpha2-workload", "code": 200, "reason": "", "UID": "2e695058-f75d-46a6-9675-224a4b9413fc", "allowed": true}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-03T13:31:49Z

In the CI? I'm not sure. When there is a problem, sometimes it cannot be reproduced locally. So it might be useful to know everything that is going on.
Although we don't use DEBUG in kueue code, so maybe it's fine.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-03T13:32:17Z

OTOH, if we find a flaky test in the CI, maybe we can reenable DEBUG.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-05-04T14:18:58Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-15T10:07:22Z

Reopen if necessary.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-15T10:07:26Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/543#issuecomment-1547568520):

>Reopen if necessary.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
