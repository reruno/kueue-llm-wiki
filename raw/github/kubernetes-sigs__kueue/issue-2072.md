# Issue #2072: makefile cant exists gsed on MacOS

**Summary**: makefile cant exists gsed on MacOS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2072

**Last updated**: 2024-05-07T12:23:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Vacant2333](https://github.com/Vacant2333)
- **Created**: 2024-04-26T05:48:31Z
- **Updated**: 2024-05-07T12:23:40Z
- **Closed**: 2024-05-07T12:23:40Z
- **Labels**: `kind/bug`
- **Assignees**: [@Vacant2333](https://github.com/Vacant2333)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
i try to install kueue in local build, but it shows 
<img width="689" alt="image" src="https://github.com/kubernetes-sigs/kueue/assets/19872346/b0870201-c0a0-49af-9e48-531f1dd99432">

and in fact i have install gsed
<img width="555" alt="image" src="https://github.com/kubernetes-sigs/kueue/assets/19872346/13b73015-d2cf-413a-b7ac-3fda07363418">


**What you expected to happen**:
i can run make
`IMAGE_REGISTRY=registry.example.com/my-user make image-local-push deploy`

**How to reproduce it (as minimally and precisely as possible)**:
OS: MacOS
`IMAGE_REGISTRY=registry.example.com/my-user make image-local-push deploy`

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

### Comment by [@Vacant2333](https://github.com/Vacant2333) — 2024-04-26T05:49:18Z

do we need fix it, i can help to create a pr :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-02T08:18:54Z

@Vacant2333 Thank you for creating this issue! Yes, this is actually a bug since we never set the `gsed` to the `SED` variable. So, could you open a PR?

https://github.com/kubernetes-sigs/kueue/blob/43e5eb8ee19fe69d3dd3f03c13f4ad46b77dd094/Makefile#L88-L94

### Comment by [@Vacant2333](https://github.com/Vacant2333) — 2024-05-02T13:14:19Z

> @Vacant2333 Thank you for creating this issue! Yes, this is actually a bug since we never set the `gsed` to the `SED` variable. So, could you open a PR?
> 
> https://github.com/kubernetes-sigs/kueue/blob/43e5eb8ee19fe69d3dd3f03c13f4ad46b77dd094/Makefile#L88-L94

yes i  will do that

/assign
