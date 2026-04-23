# Issue #9048: TAS SecondPassFailed with "insufficient unused quota" error

**Summary**: TAS SecondPassFailed with "insufficient unused quota" error

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9048

**Last updated**: 2026-02-09T08:20:32Z

---

## Metadata

- **State**: open
- **Author**: [@GonzaloSaez](https://github.com/GonzaloSaez)
- **Created**: 2026-02-07T12:03:22Z
- **Updated**: 2026-02-09T08:20:32Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I'm trying to schedule TAS workloads in GKE autopilot with kueue v0.16.0 installed via helm chart using ProvisioningRequest. When scheduling just one workload, the first pass reserves quota successfully, but the second pass fails with "insufficient unused quota". These are the events

```
3m45s       Normal    CreatedWorkload              job/gpu-test-preempt                                           Created Workload: default/job-gpu-test-preempt-7ceb1
3m44s       Normal    ProvisioningRequestCreated   workload/job-gpu-test-preempt-7ceb1                            Created ProvisioningRequest: "job-gpu-test-preempt-7ceb1-check-capacity-all-prov-1"
3m44s       Normal    QuotaReserved                workload/job-gpu-test-preempt-7ceb1                            Quota reserved in ClusterQueue gpu-cluster-queue-v1, wait time since queued was 1s
3m43s       Normal    AdmissionCheckUpdated        workload/job-gpu-test-preempt-7ceb1                            Admission check check-capacity-all-prov updated state from Pending to Ready with message: Capacity is found in the cluster
12s         Warning   SecondPassFailed             workload/job-gpu-test-preempt-7ceb1                            couldn't assign flavors to pod set main: insufficient unused quota for nvidia.com/gpu in flavor gpu-reserved-v1, 8 more needed
```

If I change the CQ so that it refers to a RF with the same spec but with no topology, the scheduling works fine (ofc there's no second pass in this case). There's only one workload running in the whole cluster, the node is fresh and has enough capacity to schedule a workload that requests 8 nvidia.com/gpu. This is the CQ status

```yaml
 status:
       admittedWorkloads: 0
       conditions:
       - lastTransitionTime: "2026-02-07T08:28:29Z"
         message: Can admit new workloads
         observedGeneration: 7
         reason: Ready
         status: "True"
         type: Active
       flavorsReservation:
       - name: gpu-reserved-v1
         resources:
         - borrowed: "0"
           name: cpu
           total: 500m
         - borrowed: "0"
           name: memory
           total: 500M
         - borrowed: "0"
           name: nvidia.com/gpu
           total: "8"
       flavorsUsage:
       - name: gpu-reserved-v1
         resources:
         - borrowed: "0"
           name: cpu
           total: "0"
         - borrowed: "0"
           name: memory
           total: "0"
         - borrowed: "0"
           name: nvidia.com/gpu
           total: "0"
       pendingWorkloads: 0
       reservingWorkloads: 1
```

**What you expected to happen**:

Second pass scheduling should not fail

**How to reproduce it (as minimally and precisely as possible)**:

GKE autopilot + kubectl apply the following

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
  kind: Topology
  metadata:
    name: topology-only-hostname
  spec:
    levels:
      - nodeLabel: kubernetes.io/hostname
  ---
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: ResourceFlavor
  metadata:
    name: gpu-reserved-v1
  spec:
    nodeLabels:
      cloud.google.com/gke-accelerator: nvidia-xxxxxx
    topologyName: topology-only-hostname
  ---
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: AdmissionCheck
  metadata:
    name: check-capacity-prov
  spec:
    controllerName: kueue.x-k8s.io/provisioning-request
    parameters:
      apiGroup: kueue.x-k8s.io
      kind: ProvisioningRequestConfig
      name: check-capacity-prov-config
  ---
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: ProvisioningRequestConfig
  metadata:
    name: check-capacity-prov-config
  spec:
    provisioningClassName: best-effort-atomic-scale-up.autoscaling.x-k8s.io
    managedResources:
      - cpu
      - memory
      - nvidia.com/gpu
  ---
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: ClusterQueue
  metadata:
    name: gpu-cluster-queue
  spec:
    queueingStrategy: StrictFIFO
    namespaceSelector: {}
    admissionChecksStrategy:
      admissionChecks:
        - name: check-capacity-prov
          onFlavors: ["gpu-reserved-v1"]
    resourceGroups:
      - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
        flavors:
          - name: gpu-reserved-v1
            resources:
              - name: cpu
                nominalQuota: "100000"
              - name: memory
                nominalQuota: 60000Gi
              - name: nvidia.com/gpu
                nominalQuota: "8"
  ---
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: LocalQueue
  metadata:
    name: gpu-local-queue
    namespace: default
  spec:
    clusterQueue: gpu-cluster-queue
---
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: test-job
    labels:
      kueue.x-k8s.io/queue-name: gpu-local-queue
    annotations:
      kueue.x-k8s.io/podset-unconstrained-topology: "true"
  spec:
    suspend: true
    template:
      spec:
        restartPolicy: Never
        containers:
          - name: test
            image: registry.k8s.io/pause:3.9
            resources:
              requests:
                cpu: "500m"
                memory: "1Gi"
                nvidia.com/gpu: 8
              limits:
                cpu: "500m"
                memory: "1Gi"
                nvidia.com/gpu: 8
```




**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.33.5
- Kueue version (use `git describe --tags --dirty --always`): v0.16.0
- Cloud provider or hardware configuration: GKE autopilot
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T08:20:32Z

Can you share the Workload status, by `kubectl get kwl <workloadname> -n<namespace> -oyaml`, and also `kubectl describe node/nodename` for one of the provisioned nodes?

I think what might be happening is that another workload is taking over the newly provisoned nodes. To prevent that you may introduce some "workload isolation" by taints and tolerations: set the 

To support workload isolation you may also need to configure `valueFromProvisioningClassDetail`. For example on GKE we support workload isolation for the queued-provisioning mode, then you should do:
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ProvisioningRequestConfig
metadata:
  name: dws-config
spec:
  provisioningClassName: queued-provisioning.gke.io
  podSetUpdates:
    nodeSelector:
    - key: autoscaling.gke.io/provisioning-request
      valueFromProvisioningClassDetail: ResizeRequestName
  managedResources:
  - nvidia.com/gpu
```
cc @yaroslava-serdiuk
