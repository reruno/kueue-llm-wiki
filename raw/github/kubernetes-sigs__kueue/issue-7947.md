# Issue #7947: [flaky test] TopologyAwareScheduling for PyTorchJob when Creating a PyTorchJob Should place pods based on the ranks-ordering

**Summary**: [flaky test] TopologyAwareScheduling for PyTorchJob when Creating a PyTorchJob Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7947

**Last updated**: 2025-11-27T13:14:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T10:54:52Z
- **Updated**: 2025-11-27T13:14:31Z
- **Closed**: 2025-11-27T13:14:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 4

## Description


**What happened**:

failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7936/pull-kueue-test-e2e-tas-release-0-13/1993989254161633280

**What you expected to happen**:
no fail
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End TAS Suite: kindest/node:v1.33.1: [It] TopologyAwareScheduling for PyTorchJob when Creating a PyTorchJob Should place pods based on the ranks-ordering expand_less	48s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:222 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-pytorch-worker-1",
                GenerateName: "",
                Namespace: "e2e-tas-pytorchjob-8xk46",
                SelfLink: "",
                UID: "dd80373b-b110-4225-9bee-61c69c46255d",
                ResourceVersion: "4945",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2025-11-27T10:38:13Z,
                },
                DeletionTimestamp: {
                    Time: 2025-11-27T10:38:44Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/podset": "worker",
                    "kueue.x-k8s.io/tas": "true",
                    "training.kubeflow.org/job-name": "ranks-pytorch",
                    "training.kubeflow.org/operator-name": "pytorchjob-controller",
                    "training.kubeflow.org/replica-index": "1",
                    "training.kubeflow.org/replica-type": "worker",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "pytorchjob-ranks-pytorch-d7bd1",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                },
                OwnerReferences: [
                    {
                        APIVersion: "kubeflow.org/v1",
                        Kind: "PyTorchJob",
                        Name: "ranks-pytorch",
                        UID: "c6c9b129-515a-40d9-a374-12aa1d4df178",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-11-27T10:38:13Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:labels\":{\".\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:training.kubeflow.org/job-name\":{},\"f:training.kubeflow.org/operator-name\":{},\"f:training.kubeflow.org/replica-index\":{},\"f:training.kubeflow.org/replica-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c6c9b129-515a-40d9-a374-12aa1d4df178\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"pytorch\\\"}\":{\".\":{},\"f:args\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"MASTER_ADDR\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"MASTER_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_MASTER_ADDR\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_MASTER_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NNODES\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NODE_RANK\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NPROC_PER_NODE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PYTHONUNBUFFERED\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RANK\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"WORLD_SIZE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}}},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:ports\":{\".\":{},\"k:{\\\"containerPort\\\":23456,\\\"protocol\\\":\\\"TCP\\\"}\":{\".\":{},\"f:containerPort\":{},\"f:name\":{},\"f:protocol\":{}}},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:example.com/gpu\":{}},\"f:requests\":{\".\":{},\"f:example.com/gpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:222 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-pytorch-worker-1",
                GenerateName: "",
                Namespace: "e2e-tas-pytorchjob-8xk46",
                SelfLink: "",
                UID: "dd80373b-b110-4225-9bee-61c69c46255d",
                ResourceVersion: "4945",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2025-11-27T10:38:13Z,
                },
                DeletionTimestamp: {
                    Time: 2025-11-27T10:38:44Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "kueue.x-k8s.io/podset": "worker",
                    "kueue.x-k8s.io/tas": "true",
                    "training.kubeflow.org/job-name": "ranks-pytorch",
                    "training.kubeflow.org/operator-name": "pytorchjob-controller",
                    "training.kubeflow.org/replica-index": "1",
                    "training.kubeflow.org/replica-type": "worker",
                },
                Annotations: {
                    "kueue.x-k8s.io/workload": "pytorchjob-ranks-pytorch-d7bd1",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                },
                OwnerReferences: [
                    {
                        APIVersion: "kubeflow.org/v1",
                        Kind: "PyTorchJob",
                        Name: "ranks-pytorch",
                        UID: "c6c9b129-515a-40d9-a374-12aa1d4df178",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-11-27T10:38:13Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:labels\":{\".\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:training.kubeflow.org/job-name\":{},\"f:training.kubeflow.org/operator-name\":{},\"f:training.kubeflow.org/replica-index\":{},\"f:training.kubeflow.org/replica-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c6c9b129-515a-40d9-a374-12aa1d4df178\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"pytorch\\\"}\":{\".\":{},\"f:args\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"MASTER_ADDR\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"MASTER_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_MASTER_ADDR\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_MASTER_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NNODES\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NODE_RANK\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PET_NPROC_PER_NODE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"PYTHONUNBUFFERED\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RANK\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"WORLD_SIZE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}}},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:ports\":{\".\":{},\"k:{\\\"containerPort\\\":23456,\\\"protocol\\\":\\\"TCP\\\"}\":{\".\":{},\"f:containerPort\":{},\"f:name\":{},\"f:protocol\":{}}},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:example.com/gpu\":{}},\"f:requests\":{\".\":{},\"f:example.com/gpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to be empty
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/pytorch_test.go:79 @ 11/27/25 10:39:00.836
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T10:54:59Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T11:27:17Z

It seems like the Pod wasn't deleted on time, the pod name is `ranks-pytorch-worker-1` based on the error message.
From [kube-scheduler logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7936/pull-kueue-test-e2e-tas-release-0-13/1993989254161633280/artifacts/run-test-tas-e2e-1.33.1/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_e0c33017b3e59b3dd8b3535f44536fc7/kube-scheduler/0.log) we see it was scheduled on `kind-worker2`, and it can be seen in the [kubelet logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7936/pull-kueue-test-e2e-tas-release-0-13/1993989254161633280/artifacts/run-test-tas-e2e-1.33.1/kind-worker2/kubelet.log)

It was eventually deleted at `10:39:01.495928     230 status_manager.go:954] "Pod fully terminated and removed from etcd"`, but this is already after the timeout for the test: `10:39:00.836`

Just 1s later, let me see what we can do about it

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T11:51:07Z

I think we can make it stable by setting low pod .spec.terminationGracePeriod, because it was terminating for 30s gracefully according to the kubelet logs (gracePeriod=30):
```
Nov 27 10:38:18 kind-worker2 kubelet[230]: I1127 10:38:18.351150     230 kubelet_pods.go:1762] "Generating pod status" podIsTerminal=false pod="e2e-tas-pytorchjob-8xk46/ranks-pytorch-worker-1"
Nov 27 10:38:18 kind-worker2 kubelet[230]: I1127 10:38:18.352043     230 kuberuntime_container.go:837] "Killing container with a grace period override" pod="e2e-tas-pytorchjob-8xk46/ranks-pytorch-worker-1" podUID="dd80373b-b110-4225-9bee-61c69c46255d" containerName="init-pytorch" containerID="containerd://20afb9c3608c67dff268de48640a79bdc3d4e28d541196e5270bdc016db03a82" gracePeriod=30
```
We already do it for some other Jobs, because we don't really care about the containers to terminate cleanly.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T11:54:12Z

/assign
