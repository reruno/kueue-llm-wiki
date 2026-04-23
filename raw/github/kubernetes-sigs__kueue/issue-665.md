# Issue #665: Error messages when MPIJob CRD is not installed

**Summary**: Error messages when MPIJob CRD is not installed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/665

**Last updated**: 2023-04-04T15:51:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-29T17:44:11Z
- **Updated**: 2023-04-04T15:51:55Z
- **Closed**: 2023-04-04T15:51:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 3

## Description

**What happened**:

Even if a user doesn't plan to use MPIJob, they might observe errors in the logs, which can be confusing.

```
{"level":"error","ts":"2023-03-29T17:21:00.928174568Z","logger":"controller-runtime.source","caller":"source/source.go:143","msg":"if kind is a CRD, it should be installed before calling Start","kind":"[MPIJob.kubeflow.org](http://mpijob.kubeflow.org/)","error":"no matches for kind \"MPIJob\" in version \"[kubeflow.org/v2beta1\](http://kubeflow.org/v2beta1%5C)"","stacktrace":"[sigs.k8s.io/controller-runtime/pkg/source.(*Kind).Start.func1.1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/source/source.go:143\nk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtectionWithContext\n\t/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:235\nk8s.io/apimachinery/pkg/util/wait.WaitForWithContext\n\t/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:662\nk8s.io/apimachinery/pkg/util/wait.poll\n\t/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:596\nk8s.io/apimachinery/pkg/util/wait.PollImmediateUntilWithContext\n\t/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:547\nsigs.k8s.io/controller-runtime/pkg/source.(*Kind).Start.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/source/source.go:136](http://sigs.k8s.io/controller-runtime/pkg/source.%28*Kind%29.Start.func1.1%5Cn%5Ct/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/source/source.go:143%5Cnk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtectionWithContext%5Cn%5Ct/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:235%5Cnk8s.io/apimachinery/pkg/util/wait.WaitForWithContext%5Cn%5Ct/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:662%5Cnk8s.io/apimachinery/pkg/util/wait.poll%5Cn%5Ct/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:596%5Cnk8s.io/apimachinery/pkg/util/wait.PollImmediateUntilWithContext%5Cn%5Ct/go/pkg/mod/k8s.io/apimachinery@v0.26.3/pkg/util/wait/wait.go:547%5Cnsigs.k8s.io/controller-runtime/pkg/source.%28*Kind%29.Start.func1%5Cn%5Ct/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/source/source.go:136)"}
```

**What you expected to happen**:

No errors. Perhaps this could be avoided by explicitly enabling MPI support via command line flag.

I wouldn't do this through the configuration API, as we plan to eventually move integrations into their own binaries.

**How to reproduce it (as minimally and precisely as possible)**:

1. Do not install mpi-operator
2. Install kueue.
3. See logs

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-29T17:44:18Z

/assign @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2023-03-30T08:06:01Z

> I wouldn't do this through the configuration API, as we plan to eventually move integrations into their own binaries.

When we split the mpi integration into a separate binary the problem will go away naturally.

Do you think we should be solving this short-term? If we are going to a short term solution we could probably supply a custom logger which filters out the message.

cc @mwielgus

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-30T13:56:22Z

/unassign @mimowo 
/assign @mwielgus
