# Issue #4544: GKE RayJob's ProvisioningRequests fail unless RayJob deleted when AdmissioCheck fails for GPU node resources

**Summary**: GKE RayJob's ProvisioningRequests fail unless RayJob deleted when AdmissioCheck fails for GPU node resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4544

**Last updated**: 2025-11-13T15:48:16Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ukclivecox](https://github.com/ukclivecox)
- **Created**: 2025-03-10T14:32:40Z
- **Updated**: 2025-11-13T15:48:16Z
- **Closed**: 2025-11-13T15:48:15Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 10

## Description

I have set a a GKE auto-scaling node-pool for GPUs with max nodes 1. If I start 3 RayJobs one will suceed but the other 2 ProvisionRequests will fail. This is solved by deleting the COMPLETED RayJob after which the ProvisionRequests can suceed. Is this expected? I would assume as the GKE node pool scales down to 0 nodes after completion of the RayJob the ProvisionRequests can succeed (1 at a time)?

Config below 

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "dws"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: AdmissionCheck
metadata:
  name: dws-prov
spec:
  controllerName: kueue.x-k8s.io/provisioning-request
  parameters:
    apiGroup: kueue.x-k8s.io
    kind: ProvisioningRequestConfig
    name: dws-config
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ProvisioningRequestConfig
metadata:
  name: dws-config
spec:
  provisioningClassName: queued-provisioning.gke.io
  managedResources:
  - nvidia.com/gpu
  retryStrategy:
    backoffLimitCount: 10
    backoffBaseSeconds: 30
    backoffMaxSeconds: 3600  
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "my-cluster-queue"
spec:
  namespaceSelector: {} 
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "ephemeral-storage"]
    flavors:
    - name: "dws"
      resources:
      - name: "cpu"
        nominalQuota: 10000  # Infinite quota.
      - name: "memory"
        nominalQuota: 10000Gi # Infinite quota.
      - name: "nvidia.com/gpu"
        nominalQuota: 1000000000  # Infinite quota.
      - name: "ephemeral-storage"
        nominalQuota: 10000Ti # Infinite quota.
  admissionChecks:
  - dws-prov
---

```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T00:35:23Z

I'm not an expert on GKE and DWS. 

> This is solved by deleting the COMPLETED RayJob

But does this mean actual Pods are already terminated?

cc @mimowo @PBundyra @mwielgus @mwysokin

### Comment by [@ukclivecox](https://github.com/ukclivecox) — 2025-03-17T18:17:40Z

Yes the pods have completed and terminated but the RayJob remains.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-03-17T19:13:25Z

Can the problem be rephrased as: if there's even one completed DWS RayJob using DWS all subsequent DWS RayJobs will fail until the successful one is deleted?

How hard would it be for you to provide a minimal reproducible example like a set of 2 yamls where one is expected to succeed and the other one is expected to fail? Is there something special about those jobs? Are they interdependent? What's in the message field in the failed RayJob/Workload? Does the failed job even reach a RayCluster before failing or will it fail before like during DWS provisioning?

Sorry for so many questions but I'm trying to narrow down search criteria.

### Comment by [@ukclivecox](https://github.com/ukclivecox) — 2025-03-17T20:20:18Z

Can try to create an example but I would hope above but with a gpu cluster with auto scaling max-nodes 1 on GKE should replicate if you try to run 2 RayJobs. It fails in the ProvisioningRequest even though the nodes have been scaled to 0 in GKE after first job completes so should allow the 2nd RayJob to start. The Jobs are not special and have the settings to delete the RayCluster after use - they each request 1 GPU.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-15T20:42:19Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-16T13:36:18Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-14T14:25:38Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-14T15:04:46Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-13T15:48:09Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-13T15:48:16Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4544#issuecomment-3528441633):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
