# Issue #3958: Kueue (v0.10.0) does not run in a restricted security namespace even though it could

**Summary**: Kueue (v0.10.0) does not run in a restricted security namespace even though it could

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3958

**Last updated**: 2025-01-13T20:19:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rhaps0dy](https://github.com/rhaps0dy)
- **Created**: 2025-01-10T22:32:40Z
- **Updated**: 2025-01-13T20:19:14Z
- **Closed**: 2025-01-13T20:19:14Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

In `main`, this is now fixable without editing the chart, because the `kube-rbac-proxy` has been removed as deprecated. **But**  it still won't work without setting the policy to be stricter in `values.yaml`, and we might as well do that by default.

I tried fixing this before with PR #2105 but @alculquicondor asked "why does root filesystem need to be writeable?" I have now investigated, and the reason is that `apiserver.crt` and `apiserver.key` are written to `/tmp`. 

I have a PR which updates #2105 , updates it with an emptyDir on `/tmp`. I will make it if it is wanted.

**What happened**:

I upgraded to kueue v0.10.0 (from my custom fork). Then, the kueue pods cannot be created because the `kube-rbac-proxy` violates the restricted podSecurityPolicy.

**What you expected to happen**:

It deploys fine.

**How to reproduce it (as minimally and precisely as possible)**:

Deploy kueue v0.10.0 using the Helm chart in a restricted security namespace. Make sure to use:
```
    podSecurityContext:
      seccompProfile:
        type: "RuntimeDefault"
      runAsNonRoot: true
    containerSecurityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-11T01:19:34Z

https://github.com/kubernetes-sigs/kueue/pull/3925

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-11T02:01:45Z

Potential duplicate: https://github.com/kubernetes-sigs/kueue/issues/3850

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2025-01-13T15:00:03Z

cc @mimowo @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-13T15:34:09Z

Actually, in 0.11 we drop `kube-rbac-proxy` completely. 

As for restricting capabilities this looks indeed like a duplicate as mentioned above. @rhaps0dy is the PR https://github.com/kubernetes-sigs/kueue/pull/3925 covering the issue?

### Comment by [@rhaps0dy](https://github.com/rhaps0dy) — 2025-01-13T20:19:14Z

Yep, PR #3925 covers it. I left a comment there that maybe should be addressed, but otherwise I'm happy.
