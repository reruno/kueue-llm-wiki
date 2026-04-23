# Issue #2665: How to avoid configuring a quota in ClusterQueue that exceeds the physical node quota？

**Summary**: How to avoid configuring a quota in ClusterQueue that exceeds the physical node quota？

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2665

**Last updated**: 2025-01-07T11:00:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@cho-chem](https://github.com/cho-chem)
- **Created**: 2024-07-22T12:35:40Z
- **Updated**: 2025-01-07T11:00:21Z
- **Closed**: 2024-07-24T03:45:03Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 5

## Description

When this situation occurs, Kueue will successfully schedule the Job, but the Pod executing the Job will remain in a pending state due to the lack of available nodes. I understand that this is not quite as expected.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-07-22T14:00:03Z

Kueue is not implementing anything that checks the configuration at that level, so in case the available resources quota are static the administrator should make sure that the configured quota is not exceeding the resources that are physically available.

What can somehow be useful in this case is using the [Kubernetes cluster-autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) [Provisioning Requests integration](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-23T10:41:48Z

@cho-chem kueue generally aims to support autoscaling clusrers where the actual resources are provisioned. Even if you use a on-premise cluster without autoscaling you could still benefit by running ProvisioningRequest with the `check-capacity.autoscaling.x-k8s.io` mode, which would check the actual capacity before admitting. Would it work for you?

### Comment by [@cho-chem](https://github.com/cho-chem) — 2024-07-24T03:44:47Z

Hi @trasc @mimowo . Thank you for your reply. The information you provided is very helpful. I will do some research on it.

### Comment by [@dafu-wu](https://github.com/dafu-wu) — 2024-12-23T07:36:05Z

@mimowo Hi,Has this function been implemented?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T11:00:19Z

Yes, the check-capacity is already supported in Kueue: https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#provisioningrequestconfig. You will need to use ClusterAutoscaler which is new enough - probably 1.31 is enough, but let me cc @yaroslava-serdiuk who may know more precisely.
