# Issue #8767: Use of Status.Patch(...patch. Apply) is deprecated in controller-runtime v0.23.0

**Summary**: Use of Status.Patch(...patch. Apply) is deprecated in controller-runtime v0.23.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8767

**Last updated**: 2026-03-09T09:23:36Z

---

## Metadata

- **State**: open
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2026-01-23T16:39:19Z
- **Updated**: 2026-03-09T09:23:36Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: [@falconlee236](https://github.com/falconlee236)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

During the manual fix to [bump controller-runtime to v0.23.0](https://github.com/kubernetes-sigs/kueue/pull/8746) we stumbled upon a deprecated `Status.Patch(...patch. Apply)`.
New version requires to use new method `Status().Apply()`.
However the method accepts `WorkloadApplyConfiguration` instead of regular `Workload`.
[The structure](https://github.com/kubernetes-sigs/kueue/blob/v0.15.3/client-go/applyconfiguration/kueue/v1beta2/workloadstatus.go) is a mirror of regular `Workload` just of a different types.

**What you expected to happen**:

IMHO there are 3 options:
1. Write a massive converter to go from `Workload` to this `WorkloadApplyConfiguration`.
2. Update each PatchStatus with alternative updateApply func.
3. Switch to Patch Merge as we plan in https://github.com/kubernetes-sigs/kueue/issues/7035.


**How to reproduce it (as minimally and precisely as possible)**:

Remove linter exception from golangci.yaml to see the problem.

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T16:49:45Z

I think (3.) is out of question for now. I'm not sure I understand (1.) or (2.). Yes, I think we should be using `Status().Apply()`, and construct `WorkloadApplyConfiguration`. I think basically we would do it based on Workload similar to our BaseSSAWorkload helper.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-23T16:59:48Z

IIRC, the previous `Apply()` function does not support any sub resource. Does the new controller-runtime support all sub resources? If yes, we can switch to the new controller-runtime `Apply()` function.

### Comment by [@alvaroaleman](https://github.com/alvaroaleman) — 2026-02-01T18:54:37Z

> IIRC, the previous Apply() function does not support any sub resource. Does the new controller-runtime support all sub resources?

Yes: https://github.com/kubernetes-sigs/controller-runtime/pull/3321

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-09T09:01:15Z

Can I try to solve this issue? @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T09:15:38Z

Yes please, go ahead 👍

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-09T09:23:35Z

/assign
