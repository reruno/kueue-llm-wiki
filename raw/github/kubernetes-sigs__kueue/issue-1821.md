# Issue #1821: RequeueState isn't always reset

**Summary**: RequeueState isn't always reset

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1821

**Last updated**: 2024-03-14T16:43:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-11T19:33:25Z
- **Updated**: 2024-03-14T16:43:56Z
- **Closed**: 2024-03-14T16:43:56Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

## Description

**What happened**:

If you introduce `g.Expect(workload.Status.RequeueState).NotTo(gomega.BeNil())` right after this line:

https://github.com/kubernetes-sigs/kueue/blob/0c5740d977f8fa73ac0c04d3007a0bf167784b9e/test/integration/webhook/workload_test.go#L109

You will see that the object already lost the RequeueState.
This is because the workload reconciler sometimes sees the old object and produces an SSA update that still has the original object with no requeueState.

I think the webhook defaulter only applies on Create and not on Update.

We should probably reset the requeueState in the reconciler itself, but I'm not sure at which point. Unless the webhook can be configured to be called during Update?

**What you expected to happen**:

RequeueState to be reset

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

I discovered this in https://github.com/kubernetes-sigs/kueue/pull/1820, when I tried to make the reconciler only do updates when the Admission condition changes.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-11T19:33:33Z

/assign @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-11T19:38:44Z

> Unless the webhook can be configured to be called during Update?

@alculquicondor We have already configure like this: https://github.com/kubernetes-sigs/kueue/blob/0c5740d977f8fa73ac0c04d3007a0bf167784b9e/config/components/webhook/manifests.yaml#L254-L274

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-11T19:39:16Z

So, maybe it seems not to work 🧐

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-13T15:54:19Z

It looks like the defaulting does work during Updates. However, webhooks cannot modify status on spec updates, or vice-versa.

So in the test API call that updates the Active field, the status.requeueState doesn't change.

But the next reconcile runs into this Status Update call:

https://github.com/kubernetes-sigs/kueue/blob/74d17e38e76c2d8b47dbea74364aecc5529f3a78/pkg/controller/core/workload_controller.go#L217

And at that point the webhook clears the requeueState.

So I think the correct action is to let the reconciler do the change, but on its dedicated API call.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-13T16:10:09Z

> It looks like the defaulting does work during Updates. However, webhooks cannot modify status on spec updates, or vice-versa.

I agree with this. Adding a test would be better.
Maybe, we can have a webhook test without launching controllers, but I'm not sure if that test is worth it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-13T16:12:31Z

> So I think the correct action is to let the reconciler do the change, but on its dedicated API call.

That sounds reasonable. Let me try it.
Thanks for sharing the results of the investigations.
