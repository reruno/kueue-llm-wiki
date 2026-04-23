# Issue #4810: Golang version selection

**Summary**: Golang version selection

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4810

**Last updated**: 2025-03-28T13:34:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rphillips](https://github.com/rphillips)
- **Created**: 2025-03-28T00:36:27Z
- **Updated**: 2025-03-28T13:34:10Z
- **Closed**: 2025-03-28T13:32:45Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What happened**:
https://github.com/kubernetes-sigs/kueue/pull/4584 bumped golang to 1.24. The project seems to still build with golang 1.23. If we bump go.mod to the latest version of golang then we are requiring all builders to upgrade to the latest version of golang, in lock-step. It is like requiring a C project to upgrade their compiler to a certain release.

Is Kueue using any golang 1.24 features? If we are, then this issue is moot. I tried compiling master today with 1.23 and it still works, so I do not believe we are using any golang 1.24 features today. 

Can we revert #4584 back to using golang 1.23?

**What you expected to happen**:
https://go.dev/doc/modules/gomod-ref states the go stanza is the minimum-go-version that can compile a project. 

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T06:14:30Z

> Is Kueue using any golang 1.24 features?

Yes for sync test.

`t.Context()`: https://github.com/kubernetes-sigs/kueue/blob/9be51c7e3563643aea96ce28b150489faa386996/pkg/cache/resource_node_test.go#L48

Additionally, we want to use latest Go version since the minor released branch will be maintained during a mostly half year.
Note Go 1.24 has been used in released Kueue branch.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-28T07:38:28Z

Note that the core k8s is also already using [1.24](https://github.com/kubernetes/kubernetes/blob/5c7491bf0874a8b292826074c13bafe1334fc7a1/go.mod#L9). 

Using 1.24 seems the right choice for Kueue, because:
- kueue is expected to move faster to meet requirements of batch workloads, and to  exercise some ideas which may later sink into the core; 
- Kueue is using k8s libraries as dependencies at compile time, some we should probably be using latest released compiler.

### Comment by [@rphillips](https://github.com/rphillips) — 2025-03-28T13:32:44Z

I'm going to close this issue. I had a chat with some K8S maintainers, and upstream is following the latest golang release due to golang deprecation requirements.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T13:34:06Z

/remove-kind bug
/kind support
