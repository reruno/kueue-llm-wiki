# Issue #4587: TAS: implicit defaulting does not work for Pod integration

**Summary**: TAS: implicit defaulting does not work for Pod integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4587

**Last updated**: 2025-03-17T09:09:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-13T09:49:07Z
- **Updated**: 2025-03-17T09:09:50Z
- **Closed**: 2025-03-17T09:09:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

The implicit defaulting of TAS annotations does not work for Pod integration.

This is because for Pod integration we rely on the topology scheduling gate. However, this gate is only added if TAS is requested explicitly: https://github.com/kubernetes-sigs/kueue/blob/1b62ba183ac0ed717119c4bb70d2e3971837c8ff/pkg/controller/jobs/pod/pod_webhook.go#L211-L214

Note that k8s validation protects against adding new scheduling gates during lifetime of a pod.

**What you expected to happen**:

TBD, some ideas are:
1. add the topology scheduling gate to all pods, allowing for "implicit" defaulting for newly created Pods - it will not help for pre-existing pods, it may also be confusing for users who don't use TAS at all.
2. drop the idea of implicit defaulting and default the scheduling type (TAS vs. non TAS) at the moment of workload creation
3. admit that implicit defaulting is not supported for the Pod integration

I would be leaning to (1.) or (2.), because there is a growing relevance of Pod integration as we use it for Deployments, STS, and LWS, so IIUC dropping support for Pod would automatically mean no support for those.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T09:51:15Z

cc @PBundyra @tenzen-y @mwielgus @mwysokin 
We didn't foresee this complication of "implicit defaulting" when solving https://github.com/kubernetes-sigs/kueue/issues/3754, but we probably need to return to the drawing board.
