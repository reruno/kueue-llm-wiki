# Issue #5039: TAS: 'couldn''t assign flavors to pod set main: no topology domains at level

**Summary**: TAS: 'couldn''t assign flavors to pod set main: no topology domains at level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5039

**Last updated**: 2025-04-18T19:39:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@OguzPastirmaci](https://github.com/OguzPastirmaci)
- **Created**: 2025-04-17T21:06:14Z
- **Updated**: 2025-04-18T19:39:20Z
- **Closed**: 2025-04-18T19:39:18Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The job doesn't start when trying to use topology aware scheduling with `'couldn''t assign flavors to pod set main: no topology domains at level: oci.oraclecloud.com/rdma.local_block_id'`. The nodes have enough free resources.

**How to reproduce it (as minimally and precisely as possible)**:

```
k get job

NAME                        STATUS      COMPLETIONS   DURATION   AGE
tas-sample-preferredk2854   Suspended   0/2                      15m
```

```
k get workload job-tas-sample-preferredk2854-590e0 -o yaml

apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2025-04-17T20:45:33Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  labels:
    kueue.x-k8s.io/job-uid: d9913b83-49fd-4808-9ecb-dc25749099ec
  name: job-tas-sample-preferredk2854-590e0
  namespace: default
  ownerReferences:
  - apiVersion: batch/v1
    blockOwnerDeletion: true
    controller: true
    kind: Job
    name: tas-sample-preferredk2854
    uid: d9913b83-49fd-4808-9ecb-dc25749099ec
  resourceVersion: "3504178"
  uid: 46b78d17-a167-452b-87b5-1b4fa4df5dc0
spec:
  active: true
  podSets:
  - count: 2
    name: main
    template:
      metadata:
        annotations:
          kueue.x-k8s.io/podset-preferred-topology: oci.oraclecloud.com/rdma.local_block_id
      spec:
        containers:
        - args:
          - pause
          image: registry.k8s.io/e2e-test-images/agnhost:2.53
          imagePullPolicy: IfNotPresent
          name: dummy-job
          resources:
            requests:
              cpu: "1"
              memory: 200Mi
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
        dnsPolicy: ClusterFirst
        restartPolicy: Never
        schedulerName: default-scheduler
        securityContext: {}
        terminationGracePeriodSeconds: 30
    topologyRequest:
      podIndexLabel: batch.kubernetes.io/job-completion-index
      preferred: oci.oraclecloud.com/rdma.local_block_id
  priority: 0
  priorityClassSource: ""
  queueName: tas-user-queue
status:
  conditions:
  - lastTransitionTime: "2025-04-17T20:45:33Z"
    message: 'couldn''t assign flavors to pod set main: no topology domains at level:
      oci.oraclecloud.com/rdma.local_block_id'
    observedGeneration: 1
    reason: Pending
    status: "False"
    type: QuotaReserved
  resourceRequests:
  - name: main
    resources:
      cpu: "2"
      memory: 400Mi
```

```
k get node -l oci.oraclecloud.com/rdma.local_block_id=5tjxbt5s6ua

NAME            STATUS   ROLES   AGE   VERSION
10.140.50.107   Ready    node    9d    v1.31.1
10.140.53.235   Ready    node    9d    v1.31.1
10.140.56.106   Ready    node    39h   v1.31.1
```

```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "oci-topology"
spec:
  levels:
  - nodeLabel: "oci.oraclecloud.com/rdma.hpc_island_id"
  - nodeLabel: "oci.oraclecloud.com/rdma.network_block_id"
  - nodeLabel: "oci.oraclecloud.com/rdma.local_block_id"
  ```

```
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta1
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    node.kubernetes.io/instance-type: "VM.Standard.E5.Flex"
  topologyName: "oci-topology"
```

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 100
      - name: "memory"
        nominalQuota: 100Gi
```

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: tas-user-queue
spec:
  clusterQueue: tas-cluster-queue
```

```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: tas-sample-preferred
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  parallelism: 2
  completions: 2
  completionMode: Indexed
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-preferred-topology: "oci.oraclecloud.com/rdma.local_block_id"
    spec:
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        args: ["pause"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31.1
- Kueue version (use `git describe --tags --dirty --always`): v.0.11.3
- Cloud provider or hardware configuration: Oracle Cloud
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): `Linux oke-cjzo2qrvfea-nli2morxp6q-sctxjmld7bq-1 6.8.0-1019-oracle #20~22.04.1-Ubuntu SMP Wed Jan 22 13:00:47 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux`

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-18T07:43:39Z

@OguzPastirmaci thank you for reporting the issue. I think I saw similar problems in the past when the nodes didn't match the RF (for example the nodeLabel, `node.kubernetes.io/instance-type: "VM.Standard.E5.Flex"`, but more generally also taints). Can you maybe check that, and possibly share the example yaml of the node?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-18T07:44:38Z

cc @mwysokin who also played testing TAS and may have recollections of this or similar scenario

### Comment by [@OguzPastirmaci](https://github.com/OguzPastirmaci) — 2025-04-18T19:23:02Z

@mimowo thank you for following up. No taints on the nodes and they all have that label. Tried using `kubernetes.io/os: "linux"` instead in the resource flavor, but got the same error.

```
k get node -l node.kubernetes.io/instance-type=VM.Standard.E5.Flex

NAME            STATUS   ROLES   AGE     VERSION
10.140.50.107   Ready    node    10d     v1.31.1
10.140.53.235   Ready    node    10d     v1.31.1
10.140.54.53    Ready    node    2d13h   v1.31.1
10.140.56.106   Ready    node    2d13h   v1.31.1
10.140.60.150   Ready    node    10d     v1.31.1
```

```
k describe node 10.140.50.107

Name:               10.140.50.107
Roles:              node
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/instance-type=VM.Standard.E5.Flex
                    beta.kubernetes.io/os=linux
                    displayName=oke-cjzo2qrvfea-nli2morxp6q-sctxjmld7bq-1
                    failure-domain.beta.kubernetes.io/region=iad
                    failure-domain.beta.kubernetes.io/zone=US-ASHBURN-AD-1
                    hostname=oke-cjzo2qrvfea-nli2morxp6q-sctxjmld7bq-1
                    internal_addr=10.140.50.107
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=10.140.50.107
                    kubernetes.io/os=linux
                    last-migration-failure=get_kubesvc_failure
                    node-role.kubernetes.io/node=
                    node.info.ds_proxymux_client=true
                    node.info/compartment.id=aaaaaaaamgpf7b5zhfwqc3cttmhatl3eqxl6uztmhozk52h2qbh4iytjvrsa
                    node.info/compartment.name=oguz
                    node.info/kubeletVersion=v1.31
                    node.kubernetes.io/instance-type=VM.Standard.E5.Flex
                    oci.oraclecloud.com/fault-domain=FAULT-DOMAIN-2
                    oci.oraclecloud.com/host.id=320e1851414
                    oci.oraclecloud.com/host.rack_id=1163795a865
                    oci.oraclecloud.com/ip-family-ipv4=true
                    oci.oraclecloud.com/ip-family-preferred=ipv4
                    oci.oraclecloud.com/node.info.managed=true
                    oci.oraclecloud.com/rdma.local_block_id=5tjxbt5s6ua
                    oci.oraclecloud.com/rdma.network_block_id=7xmzl4p4wba
                    oci.oraclecloud.com/vcn-native-ip-cni=true
                    oke.oraclecloud.com/cluster_autoscaler=disabled
                    oke.oraclecloud.com/node.info.private_subnet=true
                    oke.oraclecloud.com/node.info.private_worker=true
                    oke.oraclecloud.com/pool.mode=node-pool
                    oke.oraclecloud.com/pool.name=oke-ops
                    oke.oraclecloud.com/tf.module=terraform-oci-oke
                    oke.oraclecloud.com/tf.state_id=qrirso
                    topology.kubernetes.io/region=iad
                    topology.kubernetes.io/zone=US-ASHBURN-AD-1
                    topology.oci.com/local-block=l1
                    topology.oci.com/network-block=n1
Annotations:        alpha.kubernetes.io/provided-node-ip: 10.140.50.107
                    csi.volume.kubernetes.io/nodeid:
                      {"blockvolume.csi.oraclecloud.com":"10.140.50.107","fss.csi.oraclecloud.com":"10.140.50.107","lustre.csi.oraclecloud.com":"10.140.50.107"}
                    node.alpha.kubernetes.io/ttl: 0
                    oci.oraclecloud.com/compartment-id: ocid1.compartment.oc1..aaaaaaaamgpf7b5zhfwqc3cttmhatl3eqxl6uztmhozk52h2qbh4iytjvrsa
                    oci.oraclecloud.com/node-pool-id: ocid1.nodepool.oc1.iad.aaaaaaaa5mii6bdzr72n4wbf5fgkagxrqqfxbtktfzgkymqesnli2morxp6q
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Tue, 08 Apr 2025 18:05:46 +0000
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  10.140.50.107
  AcquireTime:     <unset>
  RenewTime:       Fri, 18 Apr 2025 19:21:27 +0000
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  MemoryPressure   False   Fri, 18 Apr 2025 19:18:40 +0000   Tue, 08 Apr 2025 18:05:46 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Fri, 18 Apr 2025 19:18:40 +0000   Tue, 08 Apr 2025 18:05:46 +0000   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Fri, 18 Apr 2025 19:18:40 +0000   Tue, 08 Apr 2025 18:05:46 +0000   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Fri, 18 Apr 2025 19:18:40 +0000   Tue, 08 Apr 2025 18:06:16 +0000   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  10.140.50.107
  Hostname:    10.140.50.107
Capacity:
  cpu:                16
  ephemeral-storage:  129886128Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             32859464Ki
  pods:               31
Allocatable:
  cpu:                15783m
  ephemeral-storage:  119703055367
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             29508936Ki
  pods:               31
System Info:
  Machine ID:                 766c3e690a01486aa746ae4fa1ab81c4
  System UUID:                65c04089-4812-44ec-bf9b-53b4d998adb7
  Boot ID:                    a403ceb5-98a9-4d5a-bcee-12e8c58d0844
  Kernel Version:             6.8.0-1019-oracle
  OS Image:                   Ubuntu 22.04.5 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  cri-o://1.31.3
  Kubelet Version:            v1.31.1
  Kube-Proxy Version:         v1.31.1
ProviderID:                   ocid1.instance.oc1.iad.anuwcljtpwneysacfkeyronlgetsvqc346gwp2lkznbvxhhguz2n2zkdm3ha
Non-terminated Pods:          (8 in total)
  Namespace                   Name                                                         CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
  ---------                   ----                                                         ------------  ----------  ---------------  -------------  ---
  kube-system                 coredns-68fd89b4f6-7xfzk                                     100m (0%)     0 (0%)      70Mi (0%)        170Mi (0%)     8d
  kube-system                 csi-oci-node-tcxlg                                           30m (0%)      500m (3%)   70Mi (0%)        300Mi (1%)     8d
  kube-system                 kube-dns-autoscaler-6cbc77b497-nhv8b                         20m (0%)      0 (0%)      10Mi (0%)        0 (0%)         8d
  kube-system                 kube-proxy-8jdkd                                             0 (0%)        0 (0%)      0 (0%)           0 (0%)         10d
  kube-system                 proxymux-client-h8x65                                        50m (0%)      500m (3%)   64Mi (0%)        256Mi (0%)     10d
  kube-system                 vcn-native-ip-cni-vf95m                                      0 (0%)        0 (0%)      0 (0%)           0 (0%)         10d
  monitoring                  kube-prometheus-stack-kube-state-metrics-77bc589946-q5xcz    0 (0%)        0 (0%)      0 (0%)           0 (0%)         10d
  monitoring                  kube-prometheus-stack-prometheus-node-exporter-xv88k         0 (0%)        0 (0%)      0 (0%)           0 (0%)         10d
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------    ------
  cpu                200m (1%)   1 (6%)
  memory             214Mi (0%)  726Mi (2%)
  ephemeral-storage  0 (0%)      0 (0%)
  hugepages-1Gi      0 (0%)      0 (0%)
  hugepages-2Mi      0 (0%)      0 (0%)
Events:              <none>
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-18T19:33:30Z

Ah, your node does not have the `hpc_island_id` label. All labels specified in the topology are required. 

I would also recommend you to configure kubernetes.io/hostname as the lowest level, because only then node taints are respected, and also because otherwise you may still suffer due to fragmentation.

### Comment by [@OguzPastirmaci](https://github.com/OguzPastirmaci) — 2025-04-18T19:39:19Z

Ah that makes sense, after adding that label now it works. I'll also add `kubernetes.io/hostname` as the lowest level.

Thanks @mimowo !
