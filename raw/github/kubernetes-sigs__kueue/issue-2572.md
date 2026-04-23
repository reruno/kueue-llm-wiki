# Issue #2572: ResourceFlavor tolerations should be included in ProvisioningRequest PodTemplate

**Summary**: ResourceFlavor tolerations should be included in ProvisioningRequest PodTemplate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2572

**Last updated**: 2024-07-17T15:53:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sam-leitch-oxb](https://github.com/sam-leitch-oxb)
- **Created**: 2024-07-10T23:34:46Z
- **Updated**: 2024-07-17T15:53:19Z
- **Closed**: 2024-07-17T15:53:19Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@PBundyra](https://github.com/PBundyra)
- **Comments**: 5

## Description

**What happened**:
I created a ResourceFlavor with a nodeSelector and tolerations that are specific to my node pool, so that when a Job is admitted to a queue with that flavor, the tolerations and nodeSelector would be added.

The ClusterQueue I'm using also has an AdmissionCheck using the provisioning-request controllerName.

My Jobs are failing because the ProvisioningRequest expects to see the toleration and nodeSelector in the PodTemplate, but they are missing.

**What you expected to happen**:
PodTemplate created for ProvisionRequest should have the nodeSelector and toleration applied. 

**How to reproduce it (as minimally and precisely as possible)**:
* Create a ResourceFlavour with a nodeSelector and toleration.
* Create a ClusterQueue and LocalQueue targeting that flavor.
* Add an AdmissionCheck with controllerName kueue.x-k8s.io/provisioning-request to the ClusterQueue flavor.
* Create a Job that does not include the nodeSelector or tolerations.
* Note the Job -> Workload -> ProvisioningRequest -> PodTemplate **does not** contain the nodeSelector or toleration.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.9
- Kueue version (use `git describe --tags --dirty --always`): 0.7.1
- Cloud provider or hardware configuration: GKE

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-12T15:20:35Z

/assign @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-16T12:36:47Z

/unassign  @PBundyra 
/assign @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-17T08:05:54Z

@sam-leitch-oxb let me ask some questions which can narrow down the investigation:
1. what is the ProvisioningRequest class name (`provisioningClassName`) you are using, is it `queued-provisioning.gke.io`? 
2. can share your config and Job with PII removed?
3. you are using 1.27.9, but the [documentation](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/) says "The Provisioning Admission Check Controller is supported on [Kubernetes cluster-autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) versions 1.29 and later. However, some cloud-providers may not have an implementation for it.". Can you test / repro on 1.29?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-17T14:48:01Z

Just to double check the basics: Did you put resource requests in the Job template?

ResourceFlavor assignment is based on the resources requested by the job template. If there are no resource requests, then there are no flavors assigned, thus no labels/tolerations.

### Comment by [@sam-leitch-oxb](https://github.com/sam-leitch-oxb) — 2024-07-17T15:53:19Z

My cluster has been updated to 1.30 and the issue appears to be resolved.
