# Issue #3099: [ClusterQueue] Provide more details about the mis-configuration in the message for Active=False

**Summary**: [ClusterQueue] Provide more details about the mis-configuration in the message for Active=False

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3099

**Last updated**: 2024-09-26T08:48:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-19T14:24:11Z
- **Updated**: 2024-09-26T08:48:02Z
- **Closed**: 2024-09-26T08:48:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 7

## Description

**What would you like to be added**:

More details in the message for the "Active=False" condition for ClusterQueue in case of mis-configuration.

Currently we have the reason field determined here: https://github.com/kubernetes-sigs/kueue/blob/82b62260d6e12d4cd1dddbdc79af711da1b1dc73/pkg/cache/clusterqueue.go#L234, but the message remains generic "Can't admit new workloads."

**Why is this needed**:

- To phrase the configuration issue in a more human-readable way, I find "FlavorIndependentAdmissionCheckAppliedPerFlavor" is hard to understand
- To provide more details which AdmissionCheck or ResourceFlavor is mis-configured, which can be handy when there are more than one.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T14:25:07Z

I believe it would be nice to complete this before https://github.com/kubernetes-sigs/kueue/issues/3095. 

/cc @alculquicondor @tenzen-y @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T14:51:01Z

+1

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T16:55:25Z

Based on the implementation the massage should already contain a concatenation of all the reasons: https://github.com/kubernetes-sigs/kueue/blob/82b62260d6e12d4cd1dddbdc79af711da1b1dc73/pkg%2Fcache%2Fclusterqueue.go#L262

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T19:03:05Z

+1

Granular messages would always be helpful for actual cluster operation.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T05:44:26Z

The message can be made more human readable and maybe include the missing flavor name, AC name and so on. Trimming it should not be necessary since it can hold 32K.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T05:44:56Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T05:53:57Z

/retitle [ClusterQueue] Provide more details about the mis-configuration in the message for Active=False
