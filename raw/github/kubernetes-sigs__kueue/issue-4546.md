# Issue #4546: Deferred setup of controller/webhook for a Kind cannot remove noop webhook

**Summary**: Deferred setup of controller/webhook for a Kind cannot remove noop webhook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4546

**Last updated**: 2025-03-11T14:07:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-03-10T20:13:42Z
- **Updated**: 2025-03-11T14:07:48Z
- **Closed**: 2025-03-11T14:07:48Z
- **Labels**: `kind/bug`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I deployed Kueue.
I waited until Kueue was running and deployed the AppWrapper controller.
The job framework's `waitForAPI` mechanisms triggered correctly because AppWrapper was now available on the API server.
However, the controller-runtime does not support _updating_ an already installed webhook.  It instead silently ignores the attempt to install a new webhook on an already covered endpoint.
As a result, Kueue's  defaulting/validating BaseWebhook were not  actually installed for the AppWrapper kind (because the noopWebhook has been installed). 
This resulted in failure to default `Suspend`.

**What you expected to happen**:

Kueue should correctly handle a Kind being added to the cluster after Kueue is installed without requiring a restart of the Kueue controller-manager.

**How to reproduce it (as minimally and precisely as possible)**:

See above description.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):  v0.11.0-devel-320-gc663d0b0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-10T20:13:54Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T08:16:31Z

> It instead silently ignores the attempt to install a new webhook on an already covered endpoint.

Oh, this is quite bad, I'm wondering how it didn't surface earlier. Are you hitting `isAlreadyHandled` in [registerDefaultingWebhook](https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/builder/webhook.go#L185-L192) and `registerValidatingWebhook`?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-11T13:15:22Z

Yes, that is the path that is taken.   I think we hadn't noticed because our e2e testing always installs the other operators before it starts Kueue's manager.   

Users didn't notice because in prior versions of Kueue, the defaulting really only mattered if manageJobsWithoutQueueName was true (which is non-default).   We run configured like this in production, but AppWrapper was an external framework so wasn't subject to the bug.   You need a built-in integration whose API is installed after Kueue and a configuration where the defaulter/validator webhooks have an observable impact to notice.
