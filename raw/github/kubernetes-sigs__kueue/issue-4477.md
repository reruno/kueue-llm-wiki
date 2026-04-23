# Issue #4477: Flaky Test: Should run an appwrapper containing a job on worker if admitted

**Summary**: Flaky Test: Should run an appwrapper containing a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4477

**Last updated**: 2025-03-04T19:23:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-03-04T15:56:40Z
- **Updated**: 2025-03-04T19:23:46Z
- **Closed**: 2025-03-04T19:23:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
End To End MultiKueue Suite: kindest/node:v1.31.2: [It] MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted 

```
{Timed out after 45.168s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:260 with:
Expected
    <[]v1.Pod | len:265, cap:292>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "job-1-t9xg5",
                GenerateName: "job-1-",
                Namespace: "multikueue-84gth",
                SelfLink: "",
                UID: "d60a5c39-83e0-4ddf-8122-b3a3ff5633d9",
                ResourceVersion: "3168",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-04T15:47:51Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/podset": "aw-0",
                    "workload.codeflare.dev/appwrapper": "aw",
                    "batch.kubernetes.io/controller-uid": "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                    "batch.kubernetes.io/job-name": "job-1",
                    "controller-uid": "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                    "job-name": "job-1",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "appwrapper-aw-6cc43",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "job-1",
                        UID: "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "batch.kubernetes.io/job-tracking",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-04T15:47:51Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:finalizers\":{\".\":{},\"v:\\\"batch.kubernetes.io/job-tracking\\\"\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/controller-uid\":{},\"f:batch.kubernetes.io/job-name\":{},\"f:controller-uid\":{},\"f:job-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:workload.codeflare.dev/appwrapper\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"d5af92f0-15a4-426f-a710-f89a5c68e25a\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-04T15:47:52Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitio...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 2 failed [FAILED] Timed out after 45.168s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:260 with:
Expected
    <[]v1.Pod | len:265, cap:292>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "job-1-t9xg5",
                GenerateName: "job-1-",
                Namespace: "multikueue-84gth",
                SelfLink: "",
                UID: "d60a5c39-83e0-4ddf-8122-b3a3ff5633d9",
                ResourceVersion: "3168",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-04T15:47:51Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/podset": "aw-0",
                    "workload.codeflare.dev/appwrapper": "aw",
                    "batch.kubernetes.io/controller-uid": "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                    "batch.kubernetes.io/job-name": "job-1",
                    "controller-uid": "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                    "job-name": "job-1",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "appwrapper-aw-6cc43",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "job-1",
                        UID: "d5af92f0-15a4-426f-a710-f89a5c68e25a",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "batch.kubernetes.io/job-tracking",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-04T15:47:51Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:finalizers\":{\".\":{},\"v:\\\"batch.kubernetes.io/job-tracking\\\"\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/controller-uid\":{},\"f:batch.kubernetes.io/job-name\":{},\"f:controller-uid\":{},\"f:job-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:workload.codeflare.dev/appwrapper\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"d5af92f0-15a4-426f-a710-f89a5c68e25a\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-04T15:47:52Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitio...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:609 @ 03/04/25 15:48:37.422
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4476/pull-kueue-test-e2e-multikueue-main/1896946183444631552

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-04T15:58:06Z

cc: @dgrove-oss

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-04T18:35:57Z

`Expected
    <[]v1.Pod | len:265, cap:292>: [
        {
`
If I'm reading this correctly, there are 265 pods in the namespace.  That would seem to suggest some rapid cycling of the pods being created by the wrapped `Job` on worker 1, but I don't see direct evidence of that in the logs.   I'm going to temporarily try to add another checking stage (#4481) and see if that helps.
