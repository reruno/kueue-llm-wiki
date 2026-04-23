# Issue #6199: https://kueue.sigs.k8s.io can not access ?

**Summary**: https://kueue.sigs.k8s.io can not access ?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6199

**Last updated**: 2025-07-28T15:07:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2025-07-28T06:48:51Z
- **Updated**: 2025-07-28T15:07:49Z
- **Closed**: 2025-07-28T15:07:48Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

https://kueue.sigs.k8s.io/

**What happened**:

<img width="1454" height="420" alt="Image" src="https://github.com/user-attachments/assets/72e362a0-dd72-480d-b96a-fc6ac7d51c28" />

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@samzong](https://github.com/samzong) — 2025-07-28T06:49:26Z

@mimowo @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T06:50:37Z

I can still access to the website.
What about private mode browser, other devices, and other web browsers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T06:51:58Z

works for me too

### Comment by [@samzong](https://github.com/samzong) — 2025-07-28T06:54:57Z

Now it's working properly. It's been almost 10 minutes since I first found the mistake.

If others have no problem, We can close this Issue later.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T07:02:44Z

Maybe there was some downtime due to redeployment of the new website version, but I'm not sure.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-28T15:07:44Z

We didn't get any report from anyone more.
So, let me close this one.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-28T15:07:49Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6199#issuecomment-3127673655):

>We didn't get any report from anyone more.
>So, let me close this one.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
