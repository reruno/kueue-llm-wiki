# Issue #3945: post-kueue-push-images job is failing on main

**Summary**: post-kueue-push-images job is failing on main

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3945

**Last updated**: 2025-01-14T05:05:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-01-08T20:31:04Z
- **Updated**: 2025-01-14T05:05:40Z
- **Closed**: 2025-01-14T02:32:28Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The latest commit has the prow job "post-kueue-push-images" failing.
**What you expected to happen**:
Job passes
**How to reproduce it (as minimally and precisely as possible)**:
Not sure.
**Anything else we need to know?**:
https://github.com/kubernetes-sigs/kueue/pull/3942 seems to have broke the job.


**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-08T20:40:11Z

This could be a flake actually. Looking at our history we are hitting a timeout with the build in rare cases. Maybe on the next merge we can see if this still occurs.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-08T20:40:39Z

I am looking at https://github.com/kubernetes-sigs/kueue/commits/main/ and checking for the red jobs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:40:50Z

Could we restart the failed Job, manually?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-08T20:45:59Z

> Could we restart the failed Job, manually?

You can see. I don't have those rights.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-08T20:48:43Z

Looking at this, I don't think this is related to the last PR. Debug images are pushed without issue and it looks to be finishing up kueue-viz. It hits the 2 hour limit which seems quite high..

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-14T02:32:24Z

/close

I think this was a infra flake.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-14T02:32:29Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3945#issuecomment-2588743966):

>/close
>
>I think this was a infra flake.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-14T05:05:38Z

> Looking at this, I don't think this is related to the last PR. Debug images are pushed without issue and it looks to be finishing up kueue-viz. It hits the 2 hour limit which seems quite high..

Thanks for the checking that. I guess that sticking and taking longer time during npm install.
