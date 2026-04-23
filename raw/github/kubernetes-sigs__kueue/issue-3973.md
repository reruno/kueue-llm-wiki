# Issue #3973: cannot generate openapi on macos

**Summary**: cannot generate openapi on macos

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3973

**Last updated**: 2025-02-17T11:19:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bobsongplus](https://github.com/bobsongplus)
- **Created**: 2025-01-15T08:02:31Z
- **Updated**: 2025-02-17T11:19:59Z
- **Closed**: 2025-02-17T11:19:57Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

 as executing  `make generate`, output the error message on Apple Sillon macOS:  `touch: setting times of '/dev/null': Permission denied  `.

**What you expected to happen**:

 `make generate` success.

**How to reproduce it (as minimally and precisely as possible)**:
 execute `make generate` on Apple Sillon macOS 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):  Darwin Kernel Version 24.2.0
- Install tools:
- Others:

## Discussion

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-15T08:04:20Z

Need to update the code-generator version after the https://github.com/kubernetes/kubernetes/pull/129629 merge.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-17T02:54:56Z

@bobsongplus It looks like the original k/k PR has been merged. So, would you mind creating PR to reflect the same fixes to the Kueue?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-17T02:56:36Z

> [@bobsongplus](https://github.com/bobsongplus) It looks like the original k/k PR has been merged. So, would you mind creating PR to reflect the same fixes to the Kueue?

NVM, we just import the script here (https://github.com/kubernetes-sigs/kueue/blob/d289679f923d5241039869fda937e549af4b55d6/hack/update-codegen.sh#L30) So, we need to wait for releasing the fixes.

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-17T03:16:28Z

> [@bobsongplus](https://github.com/bobsongplus) It looks like the original k/k PR has been merged. So, would you mind creating PR to reflect the same fixes to the Kueue?

I think so. But  I am not very quite clear on what to do next?  
 https://github.com/kubernetes-sigs/kueue/blob/d289679f923d5241039869fda937e549af4b55d6/hack/update-codegen.sh#L30

IIUC,the script `kube_codegen.sh`  called  is in $GOPATH/mod/k8s.io/code-generator which is installed by go.mod

should we update the code-generator version  in the go.mod after the kubernetes/code-generator release? Is that right ? 
@tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-17T03:25:38Z

As I mentioned in the k/k original PR, we want to backport the fix to release branch. After the patch version is released, we can use it in Kueue side.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-17T11:19:52Z

/close
resolved by #4278

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-17T11:19:57Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3973#issuecomment-2662817803):

>/close
>resolved by #4278
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
