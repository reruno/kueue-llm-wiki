# Issue #2056: Ungating pods should use patch/apply instead of update

**Summary**: Ungating pods should use patch/apply instead of update

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2056

**Last updated**: 2024-04-26T16:55:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-24T15:28:33Z
- **Updated**: 2024-04-26T16:55:58Z
- **Closed**: 2024-04-26T16:55:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

**What happened**:

When there are new fields in the Pod API, and Kueue is using an old k8s library versions, it is possible for it to drop fields that it doesn't know about when using update.

The simple solution is to use patch or server-side-apply instead.

**What you expected to happen**:

The pod integration to be resilient to k8s upgrades.

**How to reproduce it (as minimally and precisely as possible)**:

- Use k8s 1.30, kueue v0.6.x
- Enable pod integration
- Create a pod using annotation `container.apparmor.security.beta.kubernetes.io/main`

**Anything else we need to know?**:

Found in #2029

**Environment**:
- Kubernetes version (use `kubectl version`): 1.30
- Kueue version (use `git describe --tags --dirty --always`): 0.6
- Cloud provider or hardware configuration: any
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T16:27:34Z

One example of patching
https://github.com/kubernetes-sigs/kueue/commit/dddbf3db029beeee63a7417b294b2393fa5f7e5c

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T16:27:55Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-25T11:38:38Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T15:14:31Z

/unassign trasc
