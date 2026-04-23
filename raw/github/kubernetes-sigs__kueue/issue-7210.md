# Issue #7210: Kueue manifest for v0.13.6 has incorrect image reference for kueue-controller-manager

**Summary**: Kueue manifest for v0.13.6 has incorrect image reference for kueue-controller-manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7210

**Last updated**: 2025-10-10T16:34:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-10-08T17:47:13Z
- **Updated**: 2025-10-10T16:34:49Z
- **Closed**: 2025-10-10T10:02:23Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
While using the new manifest with the 0.13.6 release, Kueue controller pods fail due to `ImagePullBackoffError`
Manifest: https://github.com/kubernetes-sigs/kueue/releases/download/v0.13.6/manifests.yaml
`image: registry.k8s.io/kueue/kueue:0.13.6`

**What you expected to happen**:
The new image should be:
`image: registry.k8s.io/kueue/kueue:v0.13.6`


**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.8
- Kueue version (use `git describe --tags --dirty --always`): v0.13.6
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-09T01:47:45Z

@varunsyal Thank you for reporting that. I fixed the release artifacts, and now they should work well.
Could you check those?

```shell
$ kubectl get pod -n kueue-system
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-674c65d574-6wsh4   1/1     Running   0          99s
$ kubectl  get deployments.apps -n kueue-system kueue-controller-manager -ojsonpath="{.spec.template.spec.containers[0].image}"
registry.k8s.io/kueue/kueue:v0.13.6
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T09:03:23Z

I opened https://github.com/kubernetes-sigs/kueue/issues/7215 to prevent similar mistakes in the future

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T10:02:17Z

/close
I checked the artifacts are fixed using `image: registry.k8s.io/kueue/kueue:v0.13.6`, and did sanity testing on a live cluster.

We can open another issue if something is still missed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-10T10:02:24Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7210#issuecomment-3389164575):

>/close
>I checked the artifacts are fixed using `image: registry.k8s.io/kueue/kueue:v0.13.6`, and did sanity testing on a live cluster.
>
>We can open another issue if something is still missed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-10-10T16:34:49Z

Yes, I have confirmed that this is fixed. Thanks @tenzen-y @mimowo!
