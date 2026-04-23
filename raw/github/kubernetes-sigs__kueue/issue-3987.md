# Issue #3987: Kuberay CRDs cause crash of MultiKueue integration tests setup

**Summary**: Kuberay CRDs cause crash of MultiKueue integration tests setup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3987

**Last updated**: 2025-05-16T16:37:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-01-16T13:19:28Z
- **Updated**: 2025-05-16T16:37:12Z
- **Closed**: 2025-05-16T16:37:10Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Attempt to add CRDs of Kuberay to multikueue integration tests cause them to stuck and fail.
Integration tests CI never finishes due to reported issues.

```
  panic: Your Test Panicked
        callback[0]()
        /Users/michal_szadkowski/workspace/kueue/vendor/github.com/onsi/ginkgo/v2/internal/suite.go:323
          When you, or your assertion library, calls Ginkgo's Fail(),
          Ginkgo panics to prevent subsequent assertions from running.
  
          Normally Ginkgo rescues this panic so you shouldn't see it.
  
          However, if you make an assertion in a goroutine, Ginkgo can't capture the
          panic.
          To circumvent this, you should call
  
                defer GinkgoRecover()
  
          at the top of the goroutine that caused this panic.
```


**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

Add CRDs of Kuberay to MultiKueue integration tests in `createCluster()` as another `DepCRDPath`.

```
func createCluster(setupFnc framework.ManagerSetup, apiFeatureGates ...string) cluster {
	c := cluster{}
	c.fwk = &framework.Framework{
		CRDPath:     filepath.Join("..", "..", "..", "config", "components", "crd", "bases"),
		WebhookPath: filepath.Join("..", "..", "..", "config", "components", "webhook"),
		DepCRDPaths: []string{filepath.Join("..", "..", "..", "dep-crds", "jobset-operator"),
			filepath.Join("..", "..", "..", "dep-crds", "training-operator-crds"),
			filepath.Join("..", "..", "..", "dep-crds", "mpi-operator"),
			filepath.Join("..", "..", "..", "dep-crds", "ray-operator-crds"),
		},
		APIServerFeatureGates: apiFeatureGates,
	}
```

Minimal reproduction scenario is available in this [PR](https://github.com/kubernetes-sigs/kueue/pull/3920).


**Anything else we need to know?**:

The issue have been investigated by @mszadkow, @mbobrovskyi  and @mimowo.
The only thing that makes the tests to pass was to reduce the number of `INTEGRATION_NPROCS` which could be described as "hacky".
Also we don't know why this workaround works.

Seems that problem is solely connected to Kuberay CRDs, there were attempts to add more CRDs from different sources, which didn't cause the same issue.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-16T15:36:38Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T15:41:35Z

@mszadkow is this still the case or fixed already?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-16T16:34:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-16T16:37:05Z

/close
I believe this is fixed. @mszadkow please reopen if there is something to fix still.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-16T16:37:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3987#issuecomment-2887201554):

>/close
>I believe this is fixed. @mszadkow please reopen if there is something to fix still.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
