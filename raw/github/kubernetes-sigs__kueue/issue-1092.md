# Issue #1092: An alternate implementation of pod support with taints/tolerations

**Summary**: An alternate implementation of pod support with taints/tolerations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1092

**Last updated**: 2023-10-06T19:31:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-31T19:56:59Z
- **Updated**: 2023-10-06T19:31:46Z
- **Closed**: 2023-10-06T19:31:46Z
- **Labels**: `kind/feature`
- **Assignees**: [@nstogner](https://github.com/nstogner)
- **Comments**: 6

## Description

**What would you like to be added**:

Provide an alternate implementation for Pod support based on taints and tolerations.

I would not want to support this long term, as we have the alternate implementation using scheduling gates, which can reduce stress in kube-scheduler. Then, there should be a way for us to face out this implementation.

### Cluster Pre-requisites

In order to prevent the Pods from being scheduled, the cluster administrator needs to configure:
- The pod dispatcher to include a queue name label.
- The nodepools were queued Pods will run should have the following taints:
  - A configurable taint, for example company.com/kueue-admission. This taint mimics the behavior of a node selector.
  - NoSchedule taints with the same key and value as the nodelabels defined for the ResourceFlavor. The ResourceFlavor specs should not include these taints.

### Pod Reconciler

- For each Pod that should be managed by kueue, create a Workload object owned by the Pod.
- To implement admission, the reconciler adds:
  - a toleration matching the admission taint
  - a toleration for each node label in the ResourceFlavor where the Pod is admitted
- To implement preemption, the reconciler issues a Delete.

### Implementation alternatives

1. As a separate binary, based on #1087. This should be very easy to deprecate, but might lead to some duplicated code. It can be a great example of how people can write out-of-tree integrations.
2. As an alternate implementation of the `pkg/controller/jobs/pod`, as implemented by #1072. We can use a different build tag, so that this is not built as part of the official release. Users would need to build from source. The benefit is that we don't have to write and maintain an additional main.go
3.  As a configuration paramater to the #1072 implementation, so that it would inject tolerations instead of removing the scheduling gate and inject tolerations instead of node selectors. The configuration can be done through a command line flag that we mark as deprecated from the beginning. This option has the least duplicated code.

My take: I'm more inclined to do option 1, but maybe option 3 is not too bad if we document the maintenance guarantee properly.

**Why is this needed**:

The long term support, through scheduling gates, would only be usable in k8s clusters v1.27 or newer, limiting the adoption of Kueue.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-31T19:57:17Z

cc @tenzen-y @kerthcet WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-12T18:59:34Z

@alculquicondor Sorry for the delay in checking this. The idea sounds good to me.
I have a few concerns:

1. What happens if both pod integration with the schedulingGate and pod integration with toleration are enabled? I guess race conditions happen. So, we need to mention those integrations are exclusive in the doc.
2. What happens if the `kueue.x-k8s.io/kueue-admission` is used in the flavor nodeTaint? I guess it will cause unintended behavior for flavors. So maybe we must prohibit the same taint in flavors and admission or mention it in the doc.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-12T19:30:27Z

> What happens if both pod integration with the schedulingGate and pod integration with toleration are enabled?

Yes there would be races. But this can only happen in 1.27. Before 1.27, enabling the built-in pod integration leads to a startup failure in Kueue.

> So maybe we must prohibit the same taint in flavors and admission or mention it in the doc.

I think we should just put it in the documentation, as a limitation.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-12T19:31:06Z

cc @nstogner

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-12T19:36:42Z

> > What happens if both pod integration with the schedulingGate and pod integration with toleration are enabled?
> 
> Yes there would be races. But this can only happen in 1.27. Before 1.27, enabling the built-in pod integration leads to a startup failure in Kueue.
> 
> > So maybe we must prohibit the same taint in flavors and admission or mention it in the doc.
> 
> I think we should just put it in the documentation, as a limitation.

SGTM for adding the documentation.

### Comment by [@nstogner](https://github.com/nstogner) — 2023-10-06T19:14:47Z

/assign
