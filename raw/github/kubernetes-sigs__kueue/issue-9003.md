# Issue #9003: SanitizePodSets feature only work on containers but not on init containers

**Summary**: SanitizePodSets feature only work on containers but not on init containers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9003

**Last updated**: 2026-02-11T14:46:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@monabil08](https://github.com/monabil08)
- **Created**: 2026-02-05T12:01:21Z
- **Updated**: 2026-02-11T14:46:05Z
- **Closed**: 2026-02-11T14:46:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@monabil08](https://github.com/monabil08)
- **Comments**: 3

## Description

**What happened**:
A workload was failing in creation with the following error
```json
{"level":"error","ts":"2026-02-05T11:51:48.389945806Z","caller":"controller/controller.go:474","msg":"Reconciler error","controller":"v1_pod","namespace":"temp-ns","name":"qwe-asd-zxc","reconcileID":"d160759f-5a1f-463c-97e3-457380b014b7","error":"Workload.kueue.x-k8s.io \"pod-qwe-asd-zxc-e7fb8\" is invalid: spec.podSets[0].template.spec.initContainers[0].env[28]: Duplicate value: map[string]interface {}{\"name\":\"CPU_REQUEST\"}","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
```

**What you expected to happen**:
Given SanitizePodSets is enabled I was expecting it to deal with init containers env variables similar to normal containers and deduplicate them.

**How to reproduce it (as minimally and precisely as possible)**:
Try submitting a workload with init container, containing a duplicate env. variable

**Anything else we need to know?**:
From [the code](https://github.com/kubernetes-sigs/kueue/blob/7210ffd8e5ed4e7a0b8c26584cf5dd8dd8143fbe/pkg/controller/jobframework/utils.go#L54) it seems to be only handling containers and not init containers. Not sure if this is by design.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.33
- Kueue version (use `git describe --tags --dirty --always`): 0.15.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@monabil08](https://github.com/monabil08) — 2026-02-05T12:01:45Z

Happy to work on a fix if a member can confirm this as a bug.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T12:33:54Z

Oh yes, I think this is a bug we missed. Feel free to go ahead with the fix 👍 
cc @mbobrovskyi

### Comment by [@monabil08](https://github.com/monabil08) — 2026-02-05T13:07:59Z

/assign @monabil08
