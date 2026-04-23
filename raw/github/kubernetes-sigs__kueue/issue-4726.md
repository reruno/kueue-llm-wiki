# Issue #4726: 0.11.0 helm chart `kueueViz` nil pointer

**Summary**: 0.11.0 helm chart `kueueViz` nil pointer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4726

**Last updated**: 2025-03-21T14:44:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kafonek](https://github.com/kafonek)
- **Created**: 2025-03-20T20:42:00Z
- **Updated**: 2025-03-21T14:44:33Z
- **Closed**: 2025-03-21T14:44:33Z
- **Labels**: `kind/bug`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: 

Ran:
```
helm upgrade --install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue \
  --version=v0.11.0 \
  --namespace kueue-system \
  --set enableKueueViz=true \
  --create-namespace \
  --wait --timeout 300s
```

Error:

```
Pulled: us-central1-docker.pkg.dev/k8s-staging-images/kueue/charts/kueue:v0.11.0
Digest: sha256:d3107c3f20544cca627a7ed24597310c5464bf4acbfcc77d94dd9b546f07b038
Error: UPGRADE FAILED: template: kueue/templates/kueue-viz/frontend-deployment.yaml:19:28: executing "kueue/templates/kueue-viz/frontend-deployment.yaml" at <.Values.kueueViz.frontend.image>: nil pointer evaluating interface {}.frontend
```

**Anything else we need to know?**:

Creating a `kueueViz.frontend.image` and `kueueViz.backend.image` entry in `values.yaml` fixed the error, the defaults in the chart templates don't get used without the keys existing though.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.32.2
- Kueue version (use `git describe --tags --dirty --always`): 0.11.0 release
- Cloud provider or hardware configuration: macos docker desktop

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-20T21:17:26Z

> Creating a kueueViz.frontend.image and kueueViz.backend.image entry in values.yaml fixed the error, the defaults in the chart templates don't get used without the keys existing though.

I also can confirm this. I had a branch I forgot to push up to address this.

/assign

### Comment by [@akram](https://github.com/akram) — 2025-03-21T07:24:14Z

thank you @kafonek and @kannon92 for reporting and fixing this. I will take a look at the PR.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T10:26:46Z

/reopen 
For https://github.com/kubernetes-sigs/kueue/pull/4727

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-21T10:26:50Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4726#issuecomment-2742945635):

>/reopen 
>For https://github.com/kubernetes-sigs/kueue/pull/4727


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
