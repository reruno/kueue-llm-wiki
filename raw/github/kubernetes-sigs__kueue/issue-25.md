# Issue #25: controller.kubernetes.io/queue-name annotation not registered

**Summary**: controller.kubernetes.io/queue-name annotation not registered

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/25

**Last updated**: 2022-02-18T20:18:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sftim](https://github.com/sftim)
- **Created**: 2022-02-18T16:57:41Z
- **Updated**: 2022-02-18T20:18:23Z
- **Closed**: 2022-02-18T20:18:23Z
- **Labels**: `priority/important-soon`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 6

## Description

The code in this repo uses an annotation, `controller.kubernetes.io/queue-name`, that is not registered in https://kubernetes.io/docs/reference/labels-annotations-taints/

We should either:
- register and document the annotation
- avoid specifying `controller.kubernetes.io` as the namespace for that annotation, and instead require specifying it as a command line option to the app. That way, end-users wouldn't assume that any particular namespace is expected.
- use another namespace, that is appropriate for kueue.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T17:15:23Z

is `kueue.kubernetes.io/queue-name` acceptable?

### Comment by [@sftim](https://github.com/sftim) — 2022-02-18T17:18:41Z

I'm not 100% clear on the registration rules but it looks to me as if both `controller.kubernetes.io/queue-name` and `kueue.kubernetes.io/queue-name` are annotation keys that require registration. The Kubernetes Architecture SIG would be able to confirm what the exact requirements are for using namespaces connected with `kubernetes.io`.

### Comment by [@sftim](https://github.com/sftim) — 2022-02-18T17:19:14Z

BTW, to register an annotation, all you need to do is to document it on https://kubernetes.io/docs/reference/labels-annotations-taints/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T17:34:38Z

Let's use `kueue.x-k8s.io` for now. We will request an API review and register the annotation when we are ready for a beta API #23

We might just add queue to the Job spec instead :) https://github.com/kubernetes/kubernetes/issues/106886

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T17:35:02Z

/priority important-soon

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T17:38:43Z

/assign
