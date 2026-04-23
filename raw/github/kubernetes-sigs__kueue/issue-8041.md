# Issue #8041: KueuePopulator: Cleanup doesn't delete TAS, ClusterQueue, and ResourceFlavor

**Summary**: KueuePopulator: Cleanup doesn't delete TAS, ClusterQueue, and ResourceFlavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8041

**Last updated**: 2026-03-19T09:53:44Z

---

## Metadata

- **State**: open
- **Author**: [@Edwinhr716](https://github.com/Edwinhr716)
- **Created**: 2025-12-02T19:27:25Z
- **Updated**: 2026-03-19T09:53:44Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: I ran `helm uninstall kueue-populator --namespace kueue-system`, and later ran `kubectl get configmap -nkueue-system -oyaml` to validate that everything was deleted. However, it still shows the tas, resourceflavor, and clusterqueue yamls

```
- apiVersion: v1
  data:
    resources.yaml: |-
      apiVersion: kueue.x-k8s.io/v1beta1
      kind: Topology
      metadata:
        name: "default"
      spec:
        levels:
          - nodeLabel: "cloud.google.com/gce-topology-block"
          - nodeLabel: "cloud.google.com/gce-topology-subblock"
          - nodeLabel: "cloud.google.com/gce-topology-host"
          - nodeLabel: "kubernetes.io/hostname"
      ---
      kind: ResourceFlavor
      apiVersion: kueue.x-k8s.io/v1beta1
      metadata:
        name: "tas-gpu-default"
      spec:
        nodeLabels:
          cloud.google.com/gke-gpu: "true"
        topologyName: "default"
        tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: NoSchedule
      ---
      apiVersion: kueue.x-k8s.io/v1beta1
      kind: ClusterQueue
      metadata:
        name: "cluster-queue"
      spec:
        namespaceSelector: {} # match all.
        resourceGroups:
        - coveredResources:
          - "cpu"
          - "memory"
          - "nvidia.com/gpu"
          flavors:
          - name: "tas-gpu-default"
            resources:
            - name: "cpu"
              nominalQuota: 10
            - name: "memory"
              nominalQuota: 10Gi
            - name: "nvidia.com/gpu"
              nominalQuota: 100
  kind: ConfigMap
  metadata:
    annotations:
      helm.sh/hook: post-install,post-upgrade
      helm.sh/hook-delete-policy: before-hook-creation
      helm.sh/hook-weight: "-5"
    creationTimestamp: "2025-12-02T19:10:51Z"
    name: kueue-populator-kueue-resources
    namespace: kueue-system
    resourceVersion: "1764702651364335024"
    uid: 062fd6dd-4257-40af-8b24-9f66ce958537
kind: List
metadata:
  resourceVersion: ""
```


**What you expected to happen**: Nothing to show up

**How to reproduce it (as minimally and precisely as possible)**: Install KueuePopulator, then delete it.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-02T21:44:58Z

Helm typically does not remove CRDs and CRs upon removal of project.

This could be a feature ask for kueue-populator but I don't expect helm to uninstall these resources.

You could delete the namespace but that would only cleanup the namespaces resources in the namespace you installed too.

ref: https://helm.sh/docs/chart_best_practices/custom_resource_definitions/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T08:12:05Z

Hm, I think it might be more nuanced. The project does not create CRDs, just objects.

I suspect this the objects are not deleted on uninstall, because they are created in the post-install hooks rather than as regular objects in the template. I suspect if we created the objects during installation they would be deleted on uninstall.

cc @j-skiba wdyt?

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-12-03T08:28:51Z

Yes, I agree we could take care of deleting these in the helm chart.
We could add a new `helm.sh/hook: pre-delete` annotated hook that would delete these.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:41:44Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:24Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:53:44Z

/remove-lifecycle stale
