# Issue #4508: Flaky Test: TopologyAwareScheduling for RayJob when Creating a RayJob Should place pods based on the ranks-ordering

**Summary**: Flaky Test: TopologyAwareScheduling for RayJob when Creating a RayJob Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4508

**Last updated**: 2025-03-18T09:55:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-06T02:21:27Z
- **Updated**: 2025-03-18T09:55:51Z
- **Closed**: 2025-03-18T09:55:51Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Failed the `End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for RayJob when Creating a RayJob Should place pods based on the ranks-ordering` in periodic CI

```shell
{Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/rayjob_test.go:203 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-ray-raycluster-gpzrs-head-mm657",
                GenerateName: "ranks-ray-raycluster-gpzrs-head-",
                Namespace: "e2e-tas-rayjob-lgmbj",
                SelfLink: "",
                UID: "cbf00188-3d57-4dce-a72c-3c6827775792",
                ResourceVersion: "4265",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T22:40:41Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/tas": "true",
                    "ray.io/group": "headgroup",
                    "ray.io/identifier": "ranks-ray-raycluster-gpzrs-head",
                    "ray.io/is-ray-node": "yes",
                    "app.kubernetes.io/created-by": "kuberay-operator",
                    "kueue.x-k8s.io/podset": "head",
                    "ray.io/cluster": "ranks-ray-raycluster-gpzrs",
                    "ray.io/node-type": "head",
                    "app.kubernetes.io/name": "kuberay",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "rayjob-ranks-ray-8120c",
                    "ray.io/ft-enabled": "false",
                },
                OwnerReferences: [
                    {
                        APIVersion: "ray.io/v1",
                        Kind: "RayCluster",
                        Name: "ranks-ray-raycluster-gpzrs",
                        UID: "0616b0a6-e920-481b-9516-db1f0880f2b1",
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
                            Time: 2025-03-05T22:40:41Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:ray.io/ft-enabled\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app.kubernetes.io/created-by\":{},\"f:app.kubernetes.io/name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:ray.io/cluster\":{},\"f:ray.io/group\":{},\"f:ray.io/identifier\":{},\"f:ray.io/is-ray-node\":{},\"f:ray.io/node-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0616b0a6-e920-481b-9516-db1f0880f2b1\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"head-container\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"KUBERAY_GEN_RAY_START_CMD\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_CLOUD_INSTANCE_ID\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_CLUSTER_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ENABLE_K8S_DISK_USAGE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_NODE_TYPE_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_EXTRA_TAGS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_KUBERAY_IN_USE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"REDIS_PASSWORD\\\"}\":{\".\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 5 failed [FAILED] Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/rayjob_test.go:203 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-ray-raycluster-gpzrs-head-mm657",
                GenerateName: "ranks-ray-raycluster-gpzrs-head-",
                Namespace: "e2e-tas-rayjob-lgmbj",
                SelfLink: "",
                UID: "cbf00188-3d57-4dce-a72c-3c6827775792",
                ResourceVersion: "4265",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T22:40:41Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/tas": "true",
                    "ray.io/group": "headgroup",
                    "ray.io/identifier": "ranks-ray-raycluster-gpzrs-head",
                    "ray.io/is-ray-node": "yes",
                    "app.kubernetes.io/created-by": "kuberay-operator",
                    "kueue.x-k8s.io/podset": "head",
                    "ray.io/cluster": "ranks-ray-raycluster-gpzrs",
                    "ray.io/node-type": "head",
                    "app.kubernetes.io/name": "kuberay",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "rayjob-ranks-ray-8120c",
                    "ray.io/ft-enabled": "false",
                },
                OwnerReferences: [
                    {
                        APIVersion: "ray.io/v1",
                        Kind: "RayCluster",
                        Name: "ranks-ray-raycluster-gpzrs",
                        UID: "0616b0a6-e920-481b-9516-db1f0880f2b1",
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
                            Time: 2025-03-05T22:40:41Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:ray.io/ft-enabled\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app.kubernetes.io/created-by\":{},\"f:app.kubernetes.io/name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:ray.io/cluster\":{},\"f:ray.io/group\":{},\"f:ray.io/identifier\":{},\"f:ray.io/is-ray-node\":{},\"f:ray.io/node-type\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0616b0a6-e920-481b-9516-db1f0880f2b1\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"head-container\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"KUBERAY_GEN_RAY_START_CMD\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_CLOUD_INSTANCE_ID\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_CLUSTER_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ENABLE_K8S_DISK_USAGE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_NODE_TYPE_NAME\\\"}\":{\".\":{},\"f:name\":{},\"f:valueFrom\":{\".\":{},\"f:fieldRef\":{}}},\"k:{\\\"name\\\":\\\"RAY_PORT\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_EXTRA_TAGS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_USAGE_STATS_KUBERAY_IN_USE\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"REDIS_PASSWORD\\\"}\":{\".\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 5
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/rayjob_test.go:207 @ 03/05/25 22:45:41.951
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-tas-main/1897412525620727808

<img width="1261" alt="Image" src="https://github.com/user-attachments/assets/514c7460-678d-4d9c-b04f-c6df0a12789a" />

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-06T08:06:46Z

cc: @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T08:15:19Z

btw, the error log is truncated. I suppose one of the pods failed for some reason (and was replaced - this is why we had 5 pods). To investigate this one could follow steps similar to https://github.com/kubernetes-sigs/kueue/issues/4495. 

However, another improvement would be to increase the MaxLength for the output - currently it is too short to fit even a single Pod with status - and the status would be the most relevant case here. 

I will open a dedicated issue for that.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T08:22:07Z

Opened: https://github.com/kubernetes-sigs/kueue/issues/4509

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-06T09:52:38Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-06T09:58:16Z

This timeout again after the increase to 5 minutes...that's weird, we need to have better insight when it fails, agree

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T10:01:32Z

I think the key thing is that for some reason there was 5 pods, so probably one failed and was replaced. Try to identify the failed pod, then inspect its container logs, and logs of kubelet related to the pod (assuming the pod failure is the reason here).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T08:29:17Z

This seems like another occurrence, but on 0.10 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-tas-release-0-10/1898862090471346176

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-10T10:12:51Z

Ack, actively investigating this

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T10:36:34Z

fyi, one more: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4524/pull-kueue-test-e2e-tas-main/1899040138269298688. Seems quite often recently

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T09:57:28Z

one more: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4585/pull-kueue-test-e2e-tas-main/1900113461916995584

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-14T08:39:23Z

For this one I think we might want to change the approach.
This submitter job created by rayJob might be short lived and fall into the gap of interval.
What if we check ray cluster nodes, but later verify rayJob status, that should change after the submitter is finished anyway.
This could make it less flaky for tests while we still prove sanity of the RayJob with tas

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T10:23:11Z

I looked into the Ray failures too

First, the tests fail expecting 5 pods, but they only observe 4. Looking at the API server logs we can confirm that RayOperator only created 4:

```
> cat api.log | grep e2e-tas-rayjob-lgmbj/pods | grep POST | grep 201
2025-03-05T22:40:41.977203895Z stderr F I0305 22:40:41.976983       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods" latency="11.586316ms" userAgent="kuberay-operator/v1.2.2" audit-ID="33e27fd2-d22d-4c4d-9b46-d4efeca06f05" srcIP="172.18.0.5:37344" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="11.024848ms" resp=201
2025-03-05T22:40:42.025410431Z stderr F I0305 22:40:42.025081       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods" latency="8.426362ms" userAgent="kuberay-operator/v1.2.2" audit-ID="4d674538-ad9c-45f4-b055-dff0bd1db0a2" srcIP="172.18.0.5:37344" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="8.135949ms" resp=201
2025-03-05T22:40:42.035689969Z stderr F I0305 22:40:42.035397       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods" latency="8.717217ms" userAgent="kuberay-operator/v1.2.2" audit-ID="42111a1c-315b-47bc-a77a-aeefaa2310c2" srcIP="172.18.0.5:37344" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="8.339393ms" resp=201
2025-03-05T22:40:42.124730152Z stderr F I0305 22:40:42.124491       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods" latency="8.2536ms" userAgent="kuberay-operator/v1.2.2" audit-ID="fab4d7eb-ff9a-40cc-8cb1-d75d56f50c29" srcIP="172.18.0.5:37344" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="7.949246ms" resp=201
2025-03-05T22:40:42.999711374Z stderr F I0305 22:40:42.999502       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods/ranks-ray-raycluster-gpzrs-head-mm657/binding" latency="3.6966ms" userAgent="kube-scheduler/v1.31.1 (linux/amd64) kubernetes/948afe5/scheduler" audit-ID="1af828d9-206a-4a8a-babe-407f9529889f" srcIP="172.18.0.4:40688" apf_pl="workload-high" apf_fs="kube-scheduler" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="3.282724ms" resp=201
2025-03-05T22:40:42.999746864Z stderr F I0305 22:40:42.999677       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods/ranks-ray-raycluster-gpzrs-workers-group-0-worker-d97p4/binding" latency="3.335175ms" userAgent="kube-scheduler/v1.31.1 (linux/amd64) kubernetes/948afe5/scheduler" audit-ID="402af477-ddef-48ea-9fcf-19f58cf7eb3f" srcIP="172.18.0.4:40688" apf_pl="workload-high" apf_fs="kube-scheduler" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="2.960229ms" resp=201
2025-03-05T22:40:43.000747168Z stderr F I0305 22:40:43.000337       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods/ranks-ray-raycluster-gpzrs-workers-group-0-worker-4g6fc/binding" latency="2.859619ms" userAgent="kube-scheduler/v1.31.1 (linux/amd64) kubernetes/948afe5/scheduler" audit-ID="fe2da5fa-309d-4575-91d1-40d63398db2b" srcIP="172.18.0.4:40688" apf_pl="workload-high" apf_fs="kube-scheduler" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="2.503914ms" resp=201
2025-03-05T22:40:43.002457031Z stderr F I0305 22:40:43.002218       1 httplog.go:134] "HTTP" verb="POST" URI="/api/v1/namespaces/e2e-tas-rayjob-lgmbj/pods/ranks-ray-raycluster-gpzrs-workers-group-0-worker-zqfwn/binding" latency="4.112935ms" userAgent="kube-scheduler/v1.31.1 (linux/amd64) kubernetes/948afe5/scheduler" audit-ID="54c48759-ad7b-4b77-b91e-a565ded1429b" srcIP="172.18.0.4:40688" apf_pl="workload-high" apf_fs="kube-scheduler" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="3.769201ms" resp=201
```
Also `> cat api.log | grep e2e-tas-rayjob-lgmbj/jobs | grep POST | grep 201` returns empty indicating the Submitter Job was never created.

To give more context I grepped the kuberay operator logs which show some errors:
```
> cat ray.log | grep e2e-tas-rayjob-lgmbj               
2025-03-05T22:40:41.691025738Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.690Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.691074429Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.690Z","logger":"controllers.RayJob","msg":"Add a finalizer","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","finalizer":"ray.io/rayjob-finalizer"}
2025-03-05T22:40:41.730733001Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.730Z","logger":"controllers.RayJob","msg":"JobDeploymentStatusNew","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","RayJob":"ranks-ray"}
2025-03-05T22:40:41.730743501Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.730Z","logger":"controllers.RayJob","msg":"initRayJobStatusIfNeed","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","shouldUpdateStatus":true,"RayJob":"ranks-ray","jobId":"","rayClusterName":"","jobStatus":""}
2025-03-05T22:40:41.730750971Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.730Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","oldRayJobStatus":{"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Initializing","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.730781381Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.730Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"5a22cd41-3f27-4aa3-8a54-d8e1735be202","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"","new JobDeploymentStatus":"Initializing"}
2025-03-05T22:40:41.74035455Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.740Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.74038324Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.740Z","logger":"controllers.RayJob","msg":"JobDeploymentStatusNew","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","RayJob":"ranks-ray"}
2025-03-05T22:40:41.74039279Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.740Z","logger":"controllers.RayJob","msg":"initRayJobStatusIfNeed","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","shouldUpdateStatus":true,"RayJob":"ranks-ray","jobId":"","rayClusterName":"","jobStatus":""}
2025-03-05T22:40:41.740412Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.740Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","oldRayJobStatus":{"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobId":"ranks-ray-qcdv2","rayClusterName":"ranks-ray-raycluster-669x2","jobDeploymentStatus":"Initializing","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.74041605Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.740Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"","new JobDeploymentStatus":"Initializing"}
2025-03-05T22:40:41.747129491Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.746Z","logger":"controllers.RayJob","msg":"Failed to update RayJob status","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","error":"Operation cannot be fulfilled on rayjobs.ray.io \"ranks-ray\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-05T22:40:41.747149781Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"Warning: Reconciler returned both a non-zero result and a non-nil error. The result will always be ignored if the error is non-nil and the non-nil error causes reqeueuing with exponential backoff. For more details, see: https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile#Reconciler","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90"}
2025-03-05T22:40:41.747178671Z stderr F {"level":"error","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"Reconciler error","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"82ef785a-2582-44f0-87d6-d131e2ddee90","error":"Operation cannot be fulfilled on rayjobs.ray.io \"ranks-ray\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:227"}
2025-03-05T22:40:41.747340263Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"9ea0d50f-11cb-4f19-b0f9-67d9fae463b5","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Initializing","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.747351023Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"Try to transition the status from `Initializing` to `Suspending`","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"9ea0d50f-11cb-4f19-b0f9-67d9fae463b5","RayJob":"ranks-ray"}
2025-03-05T22:40:41.747357754Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"9ea0d50f-11cb-4f19-b0f9-67d9fae463b5","oldRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Initializing","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Suspending","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.747373524Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.747Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"9ea0d50f-11cb-4f19-b0f9-67d9fae463b5","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"Initializing","new JobDeploymentStatus":"Suspending"}
2025-03-05T22:40:41.816458069Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.816Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Initializing","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.81648789Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.816Z","logger":"controllers.RayJob","msg":"Try to transition the status from `Initializing` to `Suspending`","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","RayJob":"ranks-ray"}
2025-03-05T22:40:41.81649374Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.816Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","oldRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Initializing","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Suspending","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.81649839Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.816Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"Initializing","new JobDeploymentStatus":"Suspending"}
2025-03-05T22:40:41.82394229Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.823Z","logger":"controllers.RayJob","msg":"Failed to update RayJob status","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","error":"Operation cannot be fulfilled on rayjobs.ray.io \"ranks-ray\": the object has been modified; please apply your changes to the latest version and try again"}
2025-03-05T22:40:41.82396275Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.823Z","logger":"controllers.RayJob","msg":"Warning: Reconciler returned both a non-zero result and a non-nil error. The result will always be ignored if the error is non-nil and the non-nil error causes reqeueuing with exponential backoff. For more details, see: https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile#Reconciler","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8"}
2025-03-05T22:40:41.823982881Z stderr F {"level":"error","ts":"2025-03-05T22:40:41.823Z","logger":"controllers.RayJob","msg":"Reconciler error","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"1b4aac45-a7ca-4c4e-937d-db5893fa9ce8","error":"Operation cannot be fulfilled on rayjobs.ray.io \"ranks-ray\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/home/runner/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.5/pkg/internal/controller/controller.go:227"}
2025-03-05T22:40:41.824197244Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Suspending","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.824208124Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"The associated RayCluster for RayJob has been already deleted and it can not be found","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","RayCluster":{"name":"ranks-ray-raycluster-sr57x","namespace":"e2e-tas-rayjob-lgmbj"},"RayJob":"ranks-ray"}
2025-03-05T22:40:41.824212334Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"deleteClusterResources","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","isClusterDeleted":true}
2025-03-05T22:40:41.824235294Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"The submitter Kubernetes Job has been already deleted","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","RayJob":"ranks-ray","Kubernetes Job":""}
2025-03-05T22:40:41.824245074Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"deleteSubmitterJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","isJobDeleted":true}
2025-03-05T22:40:41.824268085Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","oldRayJobStatus":{"jobId":"ranks-ray-cmmqx","rayClusterName":"ranks-ray-raycluster-sr57x","jobDeploymentStatus":"Suspending","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobDeploymentStatus":"Suspended","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.824272795Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.824Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"f07521e0-7c67-4257-b8d3-8dc5f4dea4f5","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"Suspending","new JobDeploymentStatus":"Suspended"}
2025-03-05T22:40:41.915895512Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.915Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"e3781e9d-5a57-4d4c-b995-ee8a346246e1","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Suspended","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.915933503Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.915Z","logger":"controllers.RayJob","msg":"The status is 'Suspended', but the suspend flag is false. Transition the status to 'New'.","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"e3781e9d-5a57-4d4c-b995-ee8a346246e1"}
2025-03-05T22:40:41.915943313Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.915Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"e3781e9d-5a57-4d4c-b995-ee8a346246e1","oldRayJobStatus":{"jobDeploymentStatus":"Suspended","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.915947083Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.915Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"e3781e9d-5a57-4d4c-b995-ee8a346246e1","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"Suspended","new JobDeploymentStatus":""}
2025-03-05T22:40:41.928126647Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.927Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"d716e4ba-f93f-427b-935c-dfae9eec7d52","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.928151017Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.927Z","logger":"controllers.RayJob","msg":"JobDeploymentStatusNew","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"d716e4ba-f93f-427b-935c-dfae9eec7d52","RayJob":"ranks-ray"}
2025-03-05T22:40:41.928156777Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.927Z","logger":"controllers.RayJob","msg":"initRayJobStatusIfNeed","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"d716e4ba-f93f-427b-935c-dfae9eec7d52","shouldUpdateStatus":true,"RayJob":"ranks-ray","jobId":"","rayClusterName":"","jobStatus":""}
2025-03-05T22:40:41.928162858Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.927Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"d716e4ba-f93f-427b-935c-dfae9eec7d52","oldRayJobStatus":{"startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}},"newRayJobStatus":{"jobId":"ranks-ray-vzvd2","rayClusterName":"ranks-ray-raycluster-gpzrs","jobDeploymentStatus":"Initializing","startTime":"2025-03-05T22:40:41Z","succeeded":0,"failed":0,"rayClusterStatus":{"desiredCPU":"0","desiredMemory":"0","desiredGPU":"0","desiredTPU":"0","head":{}}}}
2025-03-05T22:40:41.928183918Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.928Z","logger":"controllers.RayJob","msg":"updateRayJobStatus","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"d716e4ba-f93f-427b-935c-dfae9eec7d52","old JobStatus":"","new JobStatus":"","old JobDeploymentStatus":"","new JobDeploymentStatus":"Initializing"}
2025-03-05T22:40:41.939842544Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.939Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Initializing","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.939879045Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.939Z","logger":"controllers.RayJob","msg":"try to find existing RayCluster instance","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","name":"ranks-ray-raycluster-gpzrs"}
2025-03-05T22:40:41.939882965Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.939Z","logger":"controllers.RayJob","msg":"RayCluster not found","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","RayJob":"ranks-ray","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"}}
2025-03-05T22:40:41.939886725Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.939Z","logger":"controllers.RayJob","msg":"RayCluster not found, creating RayCluster!","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"}}
2025-03-05T22:40:41.959965164Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.959Z","logger":"controllers.RayJob","msg":"Found the associated RayCluster for RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","RayJob":"ranks-ray","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"}}
2025-03-05T22:40:41.960283748Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayJob","msg":"Wait for the RayCluster.Status.State to be ready before submitting the job.","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"ace14a20-d46a-48ce-b78b-e792f4a93afc","RayCluster":"ranks-ray-raycluster-gpzrs","State":""}
2025-03-05T22:40:41.96039025Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayCluster","msg":"Reconciling Ingress","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2"}
2025-03-05T22:40:41.960543902Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayJob","msg":"RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"efb844e5-185c-4b5a-9702-eaf3d34be173","name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj","JobStatus":"","JobDeploymentStatus":"Initializing","SubmissionMode":"K8sJobMode"}
2025-03-05T22:40:41.960555872Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayJob","msg":"try to find existing RayCluster instance","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"efb844e5-185c-4b5a-9702-eaf3d34be173","name":"ranks-ray-raycluster-gpzrs"}
2025-03-05T22:40:41.960561152Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayJob","msg":"Found the associated RayCluster for RayJob","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"efb844e5-185c-4b5a-9702-eaf3d34be173","RayJob":"ranks-ray","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"}}
2025-03-05T22:40:41.960836436Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.960Z","logger":"controllers.RayJob","msg":"Wait for the RayCluster.Status.State to be ready before submitting the job.","RayJob":{"name":"ranks-ray","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"efb844e5-185c-4b5a-9702-eaf3d34be173","RayCluster":"ranks-ray-raycluster-gpzrs","State":""}
2025-03-05T22:40:41.964783758Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"Created service for RayCluster","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","name":"ranks-ray-raycluster-gpzrs-head-svc"}
2025-03-05T22:40:41.964833089Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"reconcilePods","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","Found 0 head Pods; creating a head Pod for the RayCluster.":"ranks-ray-raycluster-gpzrs"}
2025-03-05T22:40:41.964956361Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"head pod labels","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","labels":{"app.kubernetes.io/created-by":"kuberay-operator","app.kubernetes.io/name":"kuberay","kueue.x-k8s.io/podset":"head","kueue.x-k8s.io/tas":"true","ray.io/cluster":"ranks-ray-raycluster-gpzrs","ray.io/group":"headgroup","ray.io/identifier":"ranks-ray-raycluster-gpzrs-head","ray.io/is-ray-node":"yes","ray.io/node-type":"head"}}
2025-03-05T22:40:41.964969311Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"generateRayStartCommand","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","nodeType":"head","rayStartParams":{"block":"true","dashboard-agent-listen-port":"52365","dashboard-host":"0.0.0.0","metrics-export-port":"8080"},"Ray container resource":{"limits":{"cpu":"100m"},"requests":{"cpu":"100m"}}}
2025-03-05T22:40:41.964974551Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"generateRayStartCommand","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","rayStartCmd":"ray start --head  --num-cpus=1  --dashboard-host=0.0.0.0  --metrics-export-port=8080  --block  --dashboard-agent-listen-port=52365 "}
2025-03-05T22:40:41.964990721Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"BuildPod","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","rayNodeType":"head","generatedCmd":"ulimit -n 65536; ray start --head  --num-cpus=1  --dashboard-host=0.0.0.0  --metrics-export-port=8080  --block  --dashboard-agent-listen-port=52365 "}
2025-03-05T22:40:41.965002051Z stderr F {"level":"info","ts":"2025-03-05T22:40:41.964Z","logger":"controllers.RayCluster","msg":"Probes injection feature flag","RayCluster":{"name":"ranks-ray-raycluster-gpzrs","namespace":"e2e-tas-rayjob-lgmbj"},"reconcileID":"40c15835-bf09-4127-bb0b-cbc807ce37c2","enabled":true}
```

So some interesting logs are **The associated RayCluster for RayJob has been already deleted and it can not be found**, or **The submitter Kubernetes Job has been already deleted** at `2025-03-05T22:40:41.824` even though the kube-apiserver logs don't show any DELETE requests to the Ray APIs in this perdiod. Maybe there is some racing with the creation events not being delivered on time?

So, I expect this is actually a bug / flake in KubeRay 1.2.2. 

cc @andrewsykim have you seen something like this? If so, is this fixed in 1.3.x?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T10:23:21Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T10:27:31Z

Thank you for investigating this one. If this actually KubeRay side bug, we can skip this case until this fixes are shipped from KubeRay.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T14:32:14Z

> For this one I think we might want to change the approach.

I synced with @andrewsykim who says the issue looks "vaguely familiar", and there is some chance it is already fixed in 1.3. So instead of refactoring or relaxing tests we can just wait a bit. 

cc @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T14:34:28Z

> > For this one I think we might want to change the approach.
> 
> I synced with [@andrewsykim](https://github.com/andrewsykim) who says the issue looks "vaguely familiar", and there is some chance it is already fixed in 1.3. So instead of refactoring or relaxing tests we can just wait a bit.
> 
> cc [@mszadkow](https://github.com/mszadkow)

Thank you for letting me know.
