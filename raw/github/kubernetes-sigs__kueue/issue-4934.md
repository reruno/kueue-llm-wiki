# Issue #4934: scheduler.go uses ApplyAdmissionStatusPatch, fails on missing fields due to fieldManager

**Summary**: scheduler.go uses ApplyAdmissionStatusPatch, fails on missing fields due to fieldManager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4934

**Last updated**: 2025-04-24T08:48:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexeldeib](https://github.com/alexeldeib)
- **Created**: 2025-04-11T16:45:04Z
- **Updated**: 2025-04-24T08:48:49Z
- **Closed**: 2025-04-24T08:48:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
We get an error like this during scheduler loop
```
{"level":"error","ts":"2025-04-09T12:39:42.128555256Z","logger":"scheduler","caller":"scheduler/scheduler.go:603","msg":"Could not update Workload status","schedulingCycle":1456,"error":"Workload.kueue.x-k8s.io \"jobset-xxxxxx" is invalid: [admissionChecks[0].lastTransitionTime: Required value, admissionChecks[0].message: Required value, admissionChecks[0].state: Required value, <nil>: Invalid value: \"null\": some validation rules were not checked because the object was invalid; correct the existing errors to complete validation]","stacktrace":"sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).requeueAndUpdate\n\t/workspace/pkg/scheduler/scheduler.go:603\nsigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule\n\t/workspace/pkg/scheduler/scheduler.go:301\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1\n\t/workspace/pkg/util/wait/backoff.go:43\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:42\nsigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:34"}
```

This code manually constructs the patch rather than using the existing helper which correctly would patch admission checks and avoid the error https://github.com/kubernetes-sigs/kueue/blob/8dabaab58c4ede8adbddbee9053f2247ec9ec97e/pkg/scheduler/scheduler.go#L653-L659

the error is due to the `kueue-admission` field manager submitting an impartial patch for fields it is tracked as owner for. curiously this seems to force a failure rather than remove the field owner? I am able to provide a minimal repro of this but it requires custom ACC checks. it's possible it fails the update because there are multiple field owners (the ACC controller as well as kueue)? 

note: this is difficult to unit test with a fake client, as kueue currently uses this workaround due to fake client not fully supporting SSA https://github.com/kubernetes-sigs/kueue/blob/b6193e1932837d6d256c44257c1e1ab1a30104e3/pkg/scheduler/scheduler_test.go#L4068-L4073

the comment on the SSA helper hints at the issue https://github.com/kubernetes-sigs/kueue/blob/b6193e1932837d6d256c44257c1e1ab1a30104e3/pkg/util/testing/client.go#L148-L153

this is partly expected due to https://github.com/kubernetes-sigs/controller-runtime/issues/2341 // https://github.com/kubernetes/kubernetes/issues/115598#issuecomment-2210942918

however this leads to failed updates due to the field manager behavior, see the original error

**What you expected to happen**:

No error during patch, seems like `ApplyAdmissionStatus` already does the correct behavior, probably should just use that?

**How to reproduce it (as minimally and precisely as possible)**:

Create a jobset with ACC checks, ensure it is in a state that does not get nominated for some reason but attempts scheduling, it should hit this code path. 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.29.12 and others (n/a)
- Kueue version (use `git describe --tags --dirty --always`): v0.10.4
- Cloud provider or hardware configuration: n/a
- OS (e.g: `cat /etc/os-release`): n/a
- Kernel (e.g. `uname -a`): n/a
- Install tools: n/a
- Others: n/a
