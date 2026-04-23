# Issue #4497: Flaky test: TopologyAwareScheduling for RayJob when Creating a RayJob Should place pods based on the ranks-ordering

**Summary**: Flaky test: TopologyAwareScheduling for RayJob when Creating a RayJob Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4497

**Last updated**: 2025-03-05T13:51:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-05T09:15:33Z
- **Updated**: 2025-03-05T13:51:46Z
- **Closed**: 2025-03-05T13:51:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

/kind flake 

**What happened**:

Test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897202285335810048

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

run ci

**Anything else we need to know?**:



```
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/rayjob_test.go:202 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-ray-raycluster-knqjp-head-qw7c2",
                GenerateName: "ranks-ray-raycluster-knqjp-head-",
                Namespace: "e2e-tas-rayjob-tfhbf",
                SelfLink: "",
                UID: "128cd88a-0c33-4e9b-ace0-78e8a489353f",
                ResourceVersion: "4393",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T08:42:40Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "app.kubernetes.io/created-by": "kuberay-operator",
                    "kueue.x-k8s.io/podset": "head",
                    "ray.io/group": "headgroup",
                    "ray.io/is-ray-node": "yes",
                    "ray.io/node-type": "head",
                    "app.kubernetes.io/name": "kuberay",
                    "kueue.x-k8s.io/tas": "true",
                    "ray.io/cluster": "ranks-ray-raycluster-knqjp",
                    "ray.io/identifier": "ranks-ray-raycluster-knqjp-head",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "rayjob-ranks-ray-c3e91",
                    "ray.io/ft-enabled": "false",
                },
                OwnerReferences: [
                    {
                        APIVersion: "ray.io/v1",
                        Kind: "RayCluster",
                        Name: "ranks-ray-raycluster-knqjp",
                        UID: "53a6a117-9450-40e7-af7a-7919e2e44437",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kuberay-operator",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:42:40Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:ray.io/ft-enabled\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app.kubernetes.io/created-by\":{},\"f:app.kubernetes.io/name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:ray.io/cluster\":{},\"f:ray.io/group\":{},\"f:ray.io/identifier\":{},\"f:ray.io/is-ray-node\":{},\"f:ray.io/node-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"53a6a117-9450-40e7-af7a-7919e2e44437\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"head-container\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"KUBERAY_GEN_RAY_START_CMD\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_CLOUD_INSTANCE_ID\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_CLUSTER_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ENABLE_K8S_DISK_USAGE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_NODE_TYPE_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_EXTRA_TAGS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_KUBERAY_IN_USE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"REDIS_PASSWORD\\\"}\":{\".\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 5 failed [FAILED] Timed out after 180.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/rayjob_test.go:202 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-ray-raycluster-knqjp-head-qw7c2",
                GenerateName: "ranks-ray-raycluster-knqjp-head-",
                Namespace: "e2e-tas-rayjob-tfhbf",
                SelfLink: "",
                UID: "128cd88a-0c33-4e9b-ace0-78e8a489353f",
                ResourceVersion: "4393",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T08:42:40Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "app.kubernetes.io/created-by": "kuberay-operator",
                    "kueue.x-k8s.io/podset": "head",
                    "ray.io/group": "headgroup",
                    "ray.io/is-ray-node": "yes",
                    "ray.io/node-type": "head",
                    "app.kubernetes.io/name": "kuberay",
                    "kueue.x-k8s.io/tas": "true",
                    "ray.io/cluster": "ranks-ray-raycluster-knqjp",
                    "ray.io/identifier": "ranks-ray-raycluster-knqjp-head",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "rayjob-ranks-ray-c3e91",
                    "ray.io/ft-enabled": "false",
                },
                OwnerReferences: [
                    {
                        APIVersion: "ray.io/v1",
                        Kind: "RayCluster",
                        Name: "ranks-ray-raycluster-knqjp",
                        UID: "53a6a117-9450-40e7-af7a-7919e2e44437",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kuberay-operator",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:42:40Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:ray.io/ft-enabled\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app.kubernetes.io/created-by\":{},\"f:app.kubernetes.io/name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:ray.io/cluster\":{},\"f:ray.io/group\":{},\"f:ray.io/identifier\":{},\"f:ray.io/is-ray-node\":{},\"f:ray.io/node-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"53a6a117-9450-40e7-af7a-7919e2e44437\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"head-container\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"KUBERAY_GEN_RAY_START_CMD\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_CLOUD_INSTANCE_ID\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_CLUSTER_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ENABLE_K8S_DISK_USAGE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_NODE_TYPE_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_EXTRA_TAGS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_KUBERAY_IN_USE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"REDIS_PASSWORD\\\"}\":{\".\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 5
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/rayjob_test.go:206 @ 03/05/25 08:45:40.529
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T09:16:10Z

cc @mszadkow could it be that the 3min is not enough for Ray?
Also, I think we should call ExpectAllPodsInNamespaceDeleted in this test, but this is probably not the root cause in this case.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T09:16:30Z

cc @gabesaba
