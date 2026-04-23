# Issue #6866: Internal cert-manager error via helm install

**Summary**: Internal cert-manager error via helm install

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6866

**Last updated**: 2025-09-19T11:24:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@cmtly](https://github.com/cmtly)
- **Created**: 2025-09-16T20:14:14Z
- **Updated**: 2025-09-19T11:24:13Z
- **Closed**: 2025-09-19T11:24:13Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What happened**:
If you install kueue via helm and use a name other than kueue for the helm installation then the controller manager will error on startup. The internal cert manager throws an error as there is a mismatch in the name of the secret that it is expecting.

**What you expected to happen**:
The controller manager should start up cleanly regardless of the helm installation name.

**How to reproduce it (as minimally and precisely as possible)**:
First run a helm install:
```
$ helm install test-kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.13.4 \
  --namespace  kueue-system \
  --create-namespace
```
The controller will error on startup and enter a CrashLoopBackOff.
```
 $ k logs deployments/test-kueue-controller-manager
...
{"level":"error","ts":"2025-09-16T20:06:18.915180898Z","logger":"setup","caller":"kueue/main.go:280","msg":"Could not run manager","error":"acquiring secret to update certificates: Secret \"kueue-webhook-server-cert\" not found","errorVerbose":"Secret \"kueue-webhook-server-cert\" not found\nacquiring secret to update certificates\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded.func1\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:331\nk8s.io/apimachinery/pkg/util/wait.runConditionWithCrashProtection\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:150\nk8s.io/apimachinery/pkg/util/wait.ExponentialBackoff\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:477\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).refreshCertIfNeeded\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:364\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start\n\t/workspace/vendor/github.com/open-policy-agent/cert-controller/pkg/rotator/rotator.go:292\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/manager/runnable_group.go:226\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_arm64.s:1223","stacktrace":"main.main\n\t/workspace/cmd/kueue/main.go:280\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:283"}
```
The secret that is created does match the name of the helm installation. The controller is expecting to find `kueue-webhook-server-cert` instead of `test-kueue-webhook-server-cert`.
```
$ k get secret test-kueue-webhook-server-cert
NAME                             TYPE     DATA   AGE
test-kueue-webhook-server-cert   Opaque   0      3m58s
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.7
- Kueue version: 0.13.4 
- Install tools: helm
