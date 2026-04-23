# Issue #1125: Missmatch compatibilities with sigs.k8s.io/controller-runtime

**Summary**: Missmatch compatibilities with sigs.k8s.io/controller-runtime

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1125

**Last updated**: 2023-09-16T06:42:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@raviand](https://github.com/raviand)
- **Created**: 2023-09-15T17:20:07Z
- **Updated**: 2023-09-16T06:42:19Z
- **Closed**: 2023-09-16T06:42:18Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

I'm trying to update all the versions in a controller and I found a compatibility issue between the latest stable version of this repo
sigs.k8s.io/kueue v0.4.1
vs the latest stable version of the controller-runtime
sigs.k8s.io/controller-runtime v016.1

**What happened**:
running the controller's test
```
rvidela@LG-W-RVID402:/mnt/c/Users/rvidela/GolangProject/src/microservice-controller$ go test ./... -v
# sigs.k8s.io/kueue/pkg/config
/home/rvidela/go/pkg/mod/sigs.k8s.io/kueue@v0.4.1/pkg/config/config.go:51:7: o.MetricsBindAddress undefined (type *manager.Options has no field or method MetricsBindAddress)
/home/rvidela/go/pkg/mod/sigs.k8s.io/kueue@v0.4.1/pkg/config/config.go:52:5: o.MetricsBindAddress undefined (type *manager.Options has no field or method MetricsBindAddress)
```

**What you expected to happen**:

all tests pass without failing

**How to reproduce it (as minimally and precisely as possible)**:

run go get -u in a kubebuilder controller repo
Check versions, should see this in go.mod
sigs.k8s.io/controller-runtime v016.1
sigs.k8s.io/kueue v0.4.1

**Anything else we need to know?**:


**Environment**:
- Kubernetes version (use `kubectl version`): local test
- Kueue version (use `git describe --tags --dirty --always`): v0.4.1
- Cloud provider or hardware configuration: wsl linux system on windows
- OS (e.g: `cat /etc/os-release`): Ubuntu 20.04.3 LTS
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
/bug

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-16T06:42:14Z

This is not a bug. That error is caused by the breaking change in the controller-runtime v0.16.0. 
So, if you use kueue as a library, you must use the controller-runtime v0.15.x.

https://github.com/kubernetes-sigs/controller-runtime/releases/tag/v0.16.0

However, we will upgrade the controller-runtime version to v0.16.x in a few days, as I mentioned in https://github.com/kubernetes-sigs/kueue/issues/1054#issuecomment-1719824069.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-16T06:42:18Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1125#issuecomment-1722153979):

>This is not a bug. That error is caused by the breaking change in the controller-runtime v0.16.0. 
>So, if you use kueue as a library, you must use the controller-runtime v0.15.x.
>
>https://github.com/kubernetes-sigs/controller-runtime/releases/tag/v0.16.0
>
>However, we will upgrade the controller-runtime version to v0.16.x in a few days, as I mentioned in https://github.com/kubernetes-sigs/kueue/issues/1054#issuecomment-1719824069.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
