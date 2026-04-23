# Issue #2508: Enable Gang Scheduling on AWS EKS

**Summary**: Enable Gang Scheduling on AWS EKS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2508

**Last updated**: 2024-07-01T18:20:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@fiedlerNr9](https://github.com/fiedlerNr9)
- **Created**: 2024-07-01T01:11:59Z
- **Updated**: 2024-07-01T18:20:07Z
- **Closed**: 2024-07-01T18:20:07Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

**Context**
While considering using Kueue for Gang scheduling, it was not clear to me if all managed k8's provider are supported. When trying to run first example workloads, documented on the example of [Ray Gang scheduling on GCP](https://docs.ray.io/en/master/cluster/kubernetes/examples/rayjob-kueue-gang-scheduling.html), I was running into issues on AWS. 

For me it looks like, Kueue's `AdmissionCheck` Resource only support the following parameters spec:
```
parameters:
    apiGroup: kueue.x-k8s.io
    kind: ProvisioningRequestConfig
    name: prov-test-config
```
`ProvisioningRequestConfig` seems to leverage the [provisioning-request-crd](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/provisioning-request.md#provisioning-request-crd), which seems to be supported on GCP GKE but not on AWS EKS. Am I missing something here?

**What would you like to be added**:
- Documentation on how to enable Kueue gang scheduling on common managed k8's provider (GKE, EKS, AKS)
- AWS compatible `AdmissionCheck` kind

**Why is this needed**:
- Improving Kueue getting started experience
- Make Kueue cloud agnostic


**Completion requirements**:
- TBD


This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-07-01T05:47:08Z

Hi @fiedlerNr9 , 

The [Provisioning Admission Check Controller](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/) is not targeted to a specific cloud provider, we are just using the [ProvisioningRrequest](https://github.com/kubernetes/autoscaler/blob/4872bddce2bcc5b4a5f6a3d569111c11b8a2baf4/cluster-autoscaler/provisioningrequest/apis/autoscaling.x-k8s.io/v1beta1/types.go#L41) for which we mention that it might not be supported by all cloud providers. In my opinion Kueue is not the place to document the list of cloud providers supported by the cluster autoscaler.

The Provisioning ACC is just an optional component of a Kueue setup that can provide dynamic resource provisioning, and none of our [Run Workloads](https://kueue.sigs.k8s.io/docs/tasks/run/) guides makes any mention of it.

### Comment by [@fiedlerNr9](https://github.com/fiedlerNr9) — 2024-07-01T18:19:57Z

Hey @trasc , thanks for coming back so quickly. Agree with your points regarding this is not the place to discuss cloud providers auto scaler features. 

Your links have been really helpful - thank you!
