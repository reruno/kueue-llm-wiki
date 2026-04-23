# Issue #724: Error in run the `sample-job.yaml` in Readme

**Summary**: Error in run the `sample-job.yaml` in Readme

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/724

**Last updated**: 2023-04-26T17:01:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yankay](https://github.com/yankay)
- **Created**: 2023-04-26T07:51:11Z
- **Updated**: 2023-04-26T17:01:19Z
- **Closed**: 2023-04-26T07:54:19Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Error in run the `sample-job.yaml` in Readme at https://github.com/kubernetes-sigs/kueue/blame/main/README.md#L51

```
[root@kay171 ~]# kubectl apply -f sample-job.yaml
error: from sample-job-: cannot use generate name with apply
```

**What you expected to happen**:

It can be run successful

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):

Client Version: version.Info{Major:"1", Minor:"26", GitVersion:"v1.26.3", GitCommit:"9e644106593f3f4aa98f8a84b23db5fa378900bd", GitTreeState:"clean", BuildDate:"2023-03-15T13:40:17Z", GoVersion:"go1.19.7", Compiler:"gc", Platform:"linux/amd64"}
Kustomize Version: v4.5.7
Server Version: version.Info{Major:"1", Minor:"26", GitVersion:"v1.26.3", GitCommit:"9e644106593f3f4aa98f8a84b23db5fa378900bd", GitTreeState:"clean", BuildDate:"2023-03-15T13:33:12Z", GoVersion:"go1.19.7", Compiler:"gc", Platform:"linux/amd64"}

- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@yankay](https://github.com/yankay) — 2023-04-26T07:54:19Z

The `kubectl create -f sample-job.yaml` instead of the `kubectl apply -f sample-job.yaml` should be used.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-26T17:01:01Z

The documentation is accurate, but maybe we should clarify that `apply` wouldn't work? Up to you, if you want to send a PR with such a note.
