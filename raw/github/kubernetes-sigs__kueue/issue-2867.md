# Issue #2867: Supporting extended resources in Kueue and DWS

**Summary**: Supporting extended resources in Kueue and DWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2867

**Last updated**: 2026-04-10T07:31:21Z

---

## Metadata

- **State**: open
- **Author**: [@romilbhardwaj](https://github.com/romilbhardwaj)
- **Created**: 2024-08-21T00:59:53Z
- **Updated**: 2026-04-10T07:31:21Z
- **Closed**: —
- **Labels**: `kind/support`, `lifecycle/stale`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 23

## Description

We are using Kueue with DWS on a GKE cluster for managing GPU instances. Our [application](https://github.com/skypilot-org/skypilot) relies on accessing `/dev/fuse` exposed through a [daemonset](https://github.com/smarter-project/smarter-device-manager) that adds a extended resource `smarter-devices/fuse` to all nodes on the cluster.

If I try to submit a pod which requests the following resources ([YAML](https://gist.github.com/romilbhardwaj/3e4cd31628fbbb0f15fd05ac04c42620)):
```
    resources:
      requests:
        nvidia.com/gpu: 1
        smarter-devices/fuse: 1
      limits:
        nvidia.com/gpu: 1
        smarter-devices/fuse: 1
```

The ProvisionRequest fails with `Provisioning Request's pods cannot be scheduled in the nodepool, affected nodepools: pool-1`.  This is presumably because of the `smarter-devices/fuse` resource is not available in the node pool.

Instead of failing, I would like Kueue/DWS to provision the node and submit the pod anyway, since once the node is spin up I expect my daemonset to take care of creating the `smarter-devices/fuse` resource.

Is it possible to have Kueue/DWS "ignore" certain extended resources in the pod spec? 

More logs:
* [k describe pods](https://gist.github.com/romilbhardwaj/7c0282a8d7c9d224e9fd0b1a1e184e1e)
* [k describe workloads](https://gist.github.com/romilbhardwaj/d853688e4612cb2fdbf48d98d415dd60)
* [k describe provisioningrequest](https://gist.github.com/romilbhardwaj/215539d940641ae5e94063a68332916d)

Versions:
```
Kueue: v0.8

$ kubectl version
Client Version: v1.30.0
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.28.11-gke.1172000
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-21T15:45:07Z

Would you still want to define quotas for `smarter-devices/fuse` in Kueue?

### Comment by [@romilbhardwaj](https://github.com/romilbhardwaj) — 2024-08-21T15:59:54Z

No, we don't need quotas for `smarter-devices/fuse`. Here's an example `ClusterQueue` I would like to use:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "dws-cluster-queue"
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "smarter-devices/fuse"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 10000  # Infinite quota.
      - name: "memory"
        nominalQuota: 10000Gi # Infinite quota.
      - name: "nvidia.com/gpu"
        nominalQuota: 10  # Limited quota.
      - name: "smarter-devices/fuse"
        nominalQuota: 10000  # Infinite quota.
  admissionChecks:
  - dws-prov
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-21T16:55:45Z

We do have a field in the Kueue Configuration called `excludeResourcePrefixes` https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#Resources, but it currently only excludes them from quota calculations.

We could potentially reuse that field to also exclude them from the ProvisioningRequest creation. Or make it an additional option. But I lean towards not adding more configuration, to keep the API simple.

As a workaround, given that what you ask is not currently supported, you could always have a webhook to drops the resource from PodTemplates.

### Comment by [@colinjc](https://github.com/colinjc) — 2024-08-21T21:49:12Z

Took the webhook approach and got this working with a small Kyverno policy - 

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: mutate-dws-pod-template
  annotations:
    policies.kyverno.io/title: Remove incompatible resources from PodTemplates
    policies.kyverno.io/subject: PodTemplate
    policies.kyverno.io/description: >-
      Removes unsupported resource requests from PodTemplate manifests to allow submission to DWS queue.
spec:
  mutateExistingOnPolicyUpdate: false
  background: false
  failurePolicy: Ignore
  rules:
  - name: mutate-remove-unsupported-resources
    match:
      resources:
        kinds:
          - PodTemplate
        namespaceSelector:
          matchExpressions:
          - key: role
            operator: In
            values:
            - kueue-jobs
    mutate:
      foreach:
        - list: "request.object.template.spec.containers"
          patchesJson6902: |-
            - path: /template/spec/containers/{{elementIndex}}/resources/requests/smarter-devices~1fuse
              op: remove
            - path: /template/spec/containers/{{elementIndex}}/resources/limits/smarter-devices~1fuse
              op: remove
```

### Comment by [@romilbhardwaj](https://github.com/romilbhardwaj) — 2024-08-21T21:55:16Z

Thanks @alculquicondor. The webhook approach would work (like @colinjc's Kyverno policy), but it would be nice if Kueue could also exclude `excludeResourcePrefixes` from the PodTemplate used in the ProvisioningRequest.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T12:08:07Z

/reopen

Yes, we'll add some configuration somewhere

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T14:18:25Z

/assign @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T14:25:23Z

I think we should just remove the excluded resources from the Workload objects altogether, making sure that  equivalency checks still hold

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T18:03:27Z

@colinjc btw, don't forget to add the same rule for `request.object.template.spec.initContainers`, if you have those

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-20T18:51:05Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-21T12:53:31Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-19T12:55:10Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-21T12:56:07Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-09T09:06:12Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T09:21:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T09:23:05Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-06T09:40:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T09:46:56Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-04T10:12:10Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:30:09Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T11:05:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-09T05:55:55Z

@mimowo @gabesaba Do we still need this one?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-10T07:31:21Z

I don't know - I haven't seen this issue reported in any other channels yet, and this issue refers to a very old Kueue, also a lot could have changed at the DWS side, so before we start working on it I would like to see a repro on the latest Kueue, and new DWS.
