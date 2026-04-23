# Issue #4056: Flaky E2E Test: TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

**Summary**: Flaky E2E Test: TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4056

**Last updated**: 2025-01-30T15:39:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-01-24T15:36:12Z
- **Updated**: 2025-01-30T15:39:19Z
- **Closed**: 2025-01-30T15:39:16Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:135 with:
Expected
    <[]v1.Pod | len:5, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-jobset-replicated-job-1-0-0-q9sst",
                GenerateName: "ranks-jobset-replicated-job-1-0-0-",
                Namespace: "e2e-tas-jobset-6k9gp",
                SelfLink: "",
                UID: "482c45cc-a42b-4f4a-a226-9b8f880347cc",
                ResourceVersion: "3019",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-01-24T15:27:30Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "jobset.sigs.k8s.io/job-key": "7ad4a5ded1d0991572077f0441f867fbb0f9029f",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset": "replicated-job-1",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "job-name": "ranks-jobset-replicated-job-1-0",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "kueue.x-k8s.io/tas": "true",
                    "batch.kubernetes.io/controller-uid": "e6d80df8-868f-4b56-938c-6b053801ee10",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "batch.kubernetes.io/job-name": "ranks-jobset-replicated-job-1-0",
                    "controller-uid": "e6d80df8-868f-4b56-938c-6b053801ee10",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/job-completion-index": "0",
                },
                Annotations: {
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                    "kueue.x-k8s.io/workload": "jobset-ranks-jobset-1b87a",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/job-key": "7ad4a5ded1d0991572077f0441f867fbb0f9029f",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/job-completion-index": "0",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "ranks-jobset-replicated-job-1-0",
                        UID: "e6d80df8-868f-4b56-938c-6b053801ee10",
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
                            Time: 2025-01-24T15:27:30Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:batch.kubernetes.io/job-completion-index\":{},\"f:jobset.sigs.k8s.io/global-replicas\":{},\"f:jobset.sigs.k8s.io/job-global-index\":{},\"f:jobset.sigs.k8s.io/job-index\":{},\"f:jobset.sigs.k8s.io/job-key\":{},\"f:jobset.sigs.k8s.io/jobset-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-replicas\":{},\"f:jobset.sigs.k8s.io/restart-attempt\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:135 with:
Expected
    <[]v1.Pod | len:5, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-jobset-replicated-job-1-0-0-q9sst",
                GenerateName: "ranks-jobset-replicated-job-1-0-0-",
                Namespace: "e2e-tas-jobset-6k9gp",
                SelfLink: "",
                UID: "482c45cc-a42b-4f4a-a226-9b8f880347cc",
                ResourceVersion: "3019",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-01-24T15:27:30Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "jobset.sigs.k8s.io/job-key": "7ad4a5ded1d0991572077f0441f867fbb0f9029f",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset": "replicated-job-1",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "job-name": "ranks-jobset-replicated-job-1-0",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "kueue.x-k8s.io/tas": "true",
                    "batch.kubernetes.io/controller-uid": "e6d80df8-868f-4b56-938c-6b053801ee10",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "batch.kubernetes.io/job-name": "ranks-jobset-replicated-job-1-0",
                    "controller-uid": "e6d80df8-868f-4b56-938c-6b053801ee10",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/job-completion-index": "0",
                },
                Annotations: {
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                    "kueue.x-k8s.io/workload": "jobset-ranks-jobset-1b87a",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/job-key": "7ad4a5ded1d0991572077f0441f867fbb0f9029f",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/job-completion-index": "0",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "ranks-jobset-replicated-job-1-0",
                        UID: "e6d80df8-868f-4b56-938c-6b053801ee10",
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
                            Time: 2025-01-24T15:27:30Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:batch.kubernetes.io/job-completion-index\":{},\"f:jobset.sigs.k8s.io/global-replicas\":{},\"f:jobset.sigs.k8s.io/job-global-index\":{},\"f:jobset.sigs.k8s.io/job-index\":{},\"f:jobset.sigs.k8s.io/job-key\":{},\"f:jobset.sigs.k8s.io/jobset-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-replicas\":{},\"f:jobset.sigs.k8s.io/restart-attempt\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:136 @ 01/24/25 15:28:15.971
}
```

**What you expected to happen**:
Succeeded

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4031/pull-kueue-test-tas-e2e-main/1882809344026742784

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T16:33:57Z

@mbobrovskyi PTAL, could you also attach a link to the issue so that we can check easily the other artifacts?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T08:42:01Z

I looked at this a little bit on my own too. 

1. From [Kueue logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4031/pull-kueue-test-tas-e2e-main/1882809344026742784/artifacts/run-test-tas-e2e-1.31.1/kind-worker7/pods/kueue-system_kueue-controller-manager-d9bf7476b-h2bsb_2a0f4b34-cadb-4641-b628-cd29c7c24a65/manager/0.log) we see that all Pods were getting ungated (around `2025-01-24T15:27:31`, log lines `tas/topology_ungater.go:200 ungating pod`):
```
ranks-jobset-replicated-job-1-1-1-wx6vb kind-worker4
ranks-jobset-replicated-job-1-0-1-8kzmp kind-worker2
ranks-jobset-replicated-job-1-2-0-s6c4p kind-worker5
ranks-jobset-replicated-job-1-1-0-szp8k kind-worker3
ranks-jobset-replicated-job-1-0-0-q9sst kind-worker
ranks-jobset-replicated-job-1-2-1-47dlr kind-worker6
```
Looking at the [kube-scheduler](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4031/pull-kueue-test-tas-e2e-main/1882809344026742784/artifacts/run-test-tas-e2e-1.31.1/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_f0a53d428fc85c98c76934e7b5a93a80/kube-scheduler/0.log) logs we see that all the Pods were considered for scheduling around `2025-01-24T15:27:31`, but `ranks-jobset-replicated-job-1-0-1-8kzmp` couldn't get scheduled on `kind-worker2` due to 
```
"Unable to schedule pod; no fit; waiting" pod="e2e-tas-jobset-6k9gp/ranks-jobset-replicated-job-1-0-1-8kzmp" err="0/9 nodes are available: 1 Insufficient example.com/gpu, 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 7 node(s) didn't match Pod's node affinity/selector. preemption: 0/9 nodes are available: 1 No preemption victims found for incoming pod, 8 Preemption is not helpful for scheduling."
```
So, I assume the `example.com/gpu` resource was not available to schedule the Pod (probably still locked by the previous Job). From the kube-scheduler logs, the previous Pod scheduled to `kind-worker2` was `e2e-tas-pytorchjob-nwfg7/ranks-pytorch-worker-1`.

Looking at the kubelet logs for [kind-worker2](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4031/pull-kueue-test-tas-e2e-main/1882809344026742784/artifacts/run-test-tas-e2e-1.31.1/kind-worker2/kubelet.log) I see the Pod `e2e-tas-pytorchjob-nwfg7/ranks-pytorch-worker-1` has UID `9574ccd3-30eb-4e0c-9210-8e88ff896072`, and there are indeed traces of the Pod existing 1min later: 
```
Jan 24 15:28:28 kind-worker2 kubelet[247]: I0124 15:28:28.036119     247 reconciler_common.go:159] "operationExecutor.UnmountVolume started for volume \"kube-api-access-d7h8b\" (UniqueName: \"kubernetes.io/projected/9574ccd3-30eb-4e0c-9210-8e88ff896072-kube-api-access-d7h8b\") pod \"9574ccd3-30eb-4e0c-9210-8e88ff896072\" (UID: \"9574ccd3-30eb-4e0c-9210-8e88ff896072\") "
```
So, I suppose the deleting the Job [here](https://github.com/kubernetes-sigs/kueue/blob/b9aa1c39d0097ae24a526d41f95bf662dfe5607c/test/e2e/tas/pytorch_test.go#L80C22-L80C53) deletes the Job only, but the Pods may remain on the nodes for a while. 

So, I assume waiting a bit longer than 1min would help. I would suggest:
- trigger deletion of Pods in afterEach along with the Jobs and wait for the deletion of pods longer (either bump the LongTimeout, or introduce VeryLongTimeout=75s).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T09:44:36Z

Actually, before we increase the timeout I think it will be useful to increase the logging level for kubelet in the tests to see when actually Kubelet releases the resources. I think this should happen when the Pod transitions to terminal phase, but it is not captured by current logs. 

I would like to see these two logs:
- "Status for pod updated successfully" from [here](https://github.com/kubernetes/kubernetes/blob/8294abc599696e0d1b5aa734afa7ae1e4f5059a0/pkg/kubelet/status/status_manager.go#L920) it will tell us the transition of phase and the exit code

Example from https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/129837/pull-kubernetes-e2e-kind/1883969217045204992/artifacts/kind-worker/kubelet.log:
```
Jan 27 20:26:47 kind-worker kubelet[285]: I0127 20:26:47.141044     285 status_manager.go:920] "Status for pod updated successfully" pod="pv-1640/pod-ephm-test-secret-qmnr" statusVersion=5 status={"phase":"Failed","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-01-27T20:25:57Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-01-27T20:25:57Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-01-27T20:25:57Z","reason":"ContainersNotReady","message":"containers with unready status: [test-container-subpath-secret-qmnr]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-01-27T20:25:57Z","reason":"ContainersNotReady","message":"containers with unready status: [test-container-subpath-secret-qmnr]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-01-27T20:25:57Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"startTime":"2025-01-27T20:25:57Z","containerStatuses":[{"name":"test-container-subpath-secret-qmnr","state":{"terminated":{"exitCode":137,"reason":"ContainerStatusUnknown","message":"The container could not be located when the pod was terminated","startedAt":null,"finishedAt":null}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"","started":false,"volumeMounts":[{"name":"test-volume","mountPath":"/test-volume"},{"name":"kube-api-access-qbglk","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"BestEffort"}
```
This is V(3), but our current logging is V(2). So, I would suggest to bump the logging to V(3). I believe we could do it in the configuration for the [kind config](https://github.com/kubernetes-sigs/kueue/blob/main/hack/tas-kind-cluster.yaml), and I believe @mszadkow did it initially, but I didn't see the need back then.

Since TAS interacts closely with kube-scheduler, and thus kubelet I believe this is logs will be also useful in the future.

Any opinions @mszadkow @mbobrovskyi @PBundyra ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-29T11:54:29Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T12:19:40Z

I also looked at the older failure https://github.com/kubernetes-sigs/kueue/issues/3901 and it seems vary similar case, see my comment https://github.com/kubernetes-sigs/kueue/issues/3901#issuecomment-2621488743

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-29T13:07:56Z

I agree with mimowo and think we should first increase verbosity of logs

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T07:04:43Z

/reopen
for the other PR which increases the verbosity of logs. once this is done @mbobrovskyi let's also close the other related TAS issue.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-30T07:04:48Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4056#issuecomment-2623672439):

>/reopen
>for the other PR which increases the verbosity of logs. once this is done @mbobrovskyi let's also close the other related TAS issue.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T15:39:12Z

/close 
Actually, there is a good chance https://github.com/kubernetes-sigs/kueue/pull/4094 fixes the issue already.  Let's re-open when it occurs again. 

In the meanwhile we can track the effort of increasing the log level in a dedicated issue, opened: https://github.com/kubernetes-sigs/kueue/issues/4111

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-30T15:39:17Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4056#issuecomment-2624842571):

>/close 
>Actually, there is a good chance https://github.com/kubernetes-sigs/kueue/pull/4094 fixes the issue already.  Let's re-open when it occurs again. 
>
>In the meanwhile we can track the effort of increasing the log level in a dedicated issue, opened: https://github.com/kubernetes-sigs/kueue/issues/4111


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
