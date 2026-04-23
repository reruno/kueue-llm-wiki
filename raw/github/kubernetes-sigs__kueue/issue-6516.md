# Issue #6516: Do not require enabling Pod integration for LWS or StatefulSet

**Summary**: Do not require enabling Pod integration for LWS or StatefulSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6516

**Last updated**: 2025-10-03T08:43:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-11T07:46:39Z
- **Updated**: 2025-10-03T08:43:01Z
- **Closed**: 2025-10-03T08:43:01Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

**What would you like to be added**:

I would like not to require the dependency on PodIntegration. 

I imagine the Pod integration could be enabled at runtime for StatefulSet and LWS workloads based on the https://github.com/kubernetes-sigs/kueue/blob/6377f6539f023ed861b5e156d1be5f8cbe7ef527/pkg/controller/jobs/pod/constants/constants.go#L26 annotation.

**Why is this needed**:

1. some users may not want to run individual Pods if there is no LWS or StatefulSet managing them
2. it makes unnecessary dependency when we have new modes of running Deployments which don't require Pod integration enabled, eg. when Deployment support is added via ElasticJobs, see https://github.com/kubernetes-sigs/kueue/issues/6334

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T07:46:51Z

cc @ichekrygin @tenzen-y

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-02T12:17:25Z

/assign
