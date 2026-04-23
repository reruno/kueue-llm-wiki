# Issue #2802: kueue-dws integration, preventing pod eviction/node shutdown from low util

**Summary**: kueue-dws integration, preventing pod eviction/node shutdown from low util

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2802

**Last updated**: 2025-06-17T00:28:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@asaiacai](https://github.com/asaiacai)
- **Created**: 2024-08-08T17:44:30Z
- **Updated**: 2025-06-17T00:28:39Z
- **Closed**: 2024-08-09T10:02:07Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description

I've gotten node provisioning to work via the Kueue-DWS integration but the if my pods happen to have low CPU for 10m, the node get deprovisioned and my job fails. I have a separate lifecycle manager for the pods so it'd be nice to have the nodes/pods be alive until I explicitly terminate them. I already tried to include [cluster-autoscaler.kubernetes.io/safe-to-evict](http://cluster-autoscaler.kubernetes.io/safe-to-evict): "false" but with no success.

these were my kueue resources
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
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
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "dws-cluster-queue"
spec:
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100
    withinClusterQueue: LowerPriority
  namespaceSelector: {} 
  resourceGroups:
  - coveredResources: 
    - "cpu"
    - "memory"
    - "nvidia.com/gpu"
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 1000000  # Infinite quota.
      - name: "memory"
        nominalQuota: 1000000Gi # Infinite quota.
      - name: "nvidia.com/gpu"
        nominalQuota: 32
      - name: "smarter-devices/fuse"
        nominalQuota: 10000000
  admissionChecks:
  - dws-prov
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "dws-local-queue"
spec:
  clusterQueue: "dws-cluster-queue"
---
```

and my pod definitions
```
# Copyright 2024 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apiVersion: v1
kind: Service
metadata:
  name:  nccl-host-1
spec:
  selector:
    name:  nccl-host-1
  clusterIP: None
---
apiVersion: v1
kind: Service
metadata:
  name: nccl-host-2
spec:
  selector:
    name: nccl-host-2
  clusterIP: None
---
apiVersion: v1
kind: Pod
metadata:
  name: nccl-test-host-1
  labels:
    name: nccl-host-1
    kueue.x-k8s.io/queue-name: dws-local-queue
    kueue.x-k8s.io/pod-group-name: nccl-test
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
    cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
    provreq.kueue.x-k8s.io/maxRunDurationSeconds: "600"
    devices.gke.io/container.tcpxo-daemon: |+
      - path: /dev/nvidia0
      - path: /dev/nvidia1
      - path: /dev/nvidia2
      - path: /dev/nvidia3
      - path: /dev/nvidia4
      - path: /dev/nvidia5
      - path: /dev/nvidia6
      - path: /dev/nvidia7
      - path: /dev/nvidiactl
      - path: /dev/nvidia-uvm
      - path: /dev/dmabuf_import_helper
    networking.gke.io/default-interface: 'eth0'
    networking.gke.io/interfaces: |
      [
        {"interfaceName":"eth0","network":"default"},
        {"interfaceName":"eth1","network":"vpc1"},
        {"interfaceName":"eth2","network":"vpc2"},
        {"interfaceName":"eth3","network":"vpc3"},
        {"interfaceName":"eth4","network":"vpc4"},
        {"interfaceName":"eth5","network":"vpc5"},
        {"interfaceName":"eth6","network":"vpc6"},
        {"interfaceName":"eth7","network":"vpc7"},
        {"interfaceName":"eth8","network":"vpc8"}
      ]
spec:
  hostname: host1
  subdomain: nccl-host-1
  #  hostNetwork: true
  #  dnsPolicy: ClusterFirstWithHostNet
  nodeSelector:
    cloud.google.com/gke-nodepool: a3-pool 
  containers:
    - name: tcpxo-daemon
      image: us-docker.pkg.dev/gce-ai-infra/gpudirect-tcpxo/tcpgpudmarxd-dev:v1.0.9
      imagePullPolicy: Always
      command: ["/bin/sh", "-c"]
      args:
        - |
          set -ex
          chmod 755 /fts/entrypoint_rxdm_container.sh
          /fts/entrypoint_rxdm_container.sh --num_hops=2 --num_nics=8 --uid= --alsologtostderr
      securityContext:
        #        privileged: true
        capabilities:
          add:
            - NET_ADMIN
            - NET_BIND_SERVICE
      volumeMounts:
        - name: nvidia
          mountPath: /usr/local/nvidia/lib64
        - name: sys
          mountPath: /hostsysfs
        - name: proc-sys
          mountPath: /hostprocsysfs
      env:
        - name: LD_LIBRARY_PATH
          value: /usr/local/nvidia/lib64
    - name: nccl-test
      image: us-docker.pkg.dev/gce-ai-infra/gpudirect-tcpxo/nccl-plugin-gpudirecttcpx-dev:v1.0.3
      imagePullPolicy: Always
      #      securityContext:
      #        privileged: true
      command:
        - /bin/sh
        - -c
        - |
          set -ex
          chmod 755  /scripts/demo-run-nccl-test-tcpxo-via-mpi.sh
          cat >/scripts/allgather.sh <<EOF
          #!/bin/bash
          /scripts/init_ssh.sh \${@};
          pushd /scripts;
          /scripts/gen_hostfiles.sh \${@};
          popd;
          BENCHMARK=all_gather_perf NHOSTS=2 NCCL_LIB_DIR="${LD_LIBRARY_PATH}" LD_LIBRARY_PATH="${LD_LIBRARY_PATH}" /scripts/demo-run-nccl-test-tcpxo-via-mpi.sh
          EOF
          chmod +x /scripts/allgather.sh
          service ssh restart;
          sleep infinity;
      env:
        - name: LD_LIBRARY_PATH
          value: /usr/local/nvidia/lib64
        - name: NCCL_FASTRAK_LLCM_DEVICE_DIRECTORY
          value: /dev/aperture_devices
      volumeMounts:
        - name: nvidia
          mountPath: /usr/local/nvidia/lib64
        - name: shared-memory
          mountPath: /dev/shm
        - name: aperture-devices
          mountPath: /dev/aperture_devices
      resources:
        limits:
          nvidia.com/gpu: 8
  volumes:
    - name: nvidia
      hostPath:
        path: /home/kubernetes/bin/nvidia/lib64
    - name: shared-memory
      emptyDir:
        medium: "Memory"
        sizeLimit: 1Gi
    - name: sys
      hostPath:
        path: /sys
    - name: proc-sys
      hostPath:
        path: /proc/sys
    - name: aperture-devices
      hostPath:
        path: /dev/aperture_devices

---
apiVersion: v1
kind: Pod
metadata:
  name: nccl-test-host-2
  labels:
    name: nccl-host-2
    kueue.x-k8s.io/queue-name: dws-local-queue
    kueue.x-k8s.io/pod-group-name: nccl-test
  annotations:
    provreq.kueue.x-k8s.io/maxRunDurationSeconds: "600"
    kueue.x-k8s.io/pod-group-total-count: "2"
    cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
    devices.gke.io/container.tcpxo-daemon: |+
      - path: /dev/nvidia0
      - path: /dev/nvidia1
      - path: /dev/nvidia2
      - path: /dev/nvidia3
      - path: /dev/nvidia4
      - path: /dev/nvidia5
      - path: /dev/nvidia6
      - path: /dev/nvidia7
      - path: /dev/nvidiactl
      - path: /dev/nvidia-uvm
      - path: /dev/dmabuf_import_helper
    networking.gke.io/default-interface: 'eth0'
    networking.gke.io/interfaces: |
      [
        {"interfaceName":"eth0","network":"default"},
        {"interfaceName":"eth1","network":"vpc1"},
        {"interfaceName":"eth2","network":"vpc2"},
        {"interfaceName":"eth3","network":"vpc3"},
        {"interfaceName":"eth4","network":"vpc4"},
        {"interfaceName":"eth5","network":"vpc5"},
        {"interfaceName":"eth6","network":"vpc6"},
        {"interfaceName":"eth7","network":"vpc7"},
        {"interfaceName":"eth8","network":"vpc8"}
      ]
spec:
  hostname: host2
  subdomain: nccl-host-2
  #  hostNetwork: true
  #  dnsPolicy: ClusterFirstWithHostNet
  nodeSelector:
    cloud.google.com/gke-nodepool: a3-pool 
  containers:
    - name: tcpxo-daemon
      image: us-docker.pkg.dev/gce-ai-infra/gpudirect-tcpxo/tcpgpudmarxd-dev:v1.0.9
      imagePullPolicy: Always
      command: ["/bin/sh", "-c"]
      args:
        - |
          set -ex
          chmod 755 /fts/entrypoint_rxdm_container.sh
          /fts/entrypoint_rxdm_container.sh --num_hops=2 --num_nics=8 --uid= --alsologtostderr
      securityContext:
        #        privileged: true
        capabilities:
          add:
            - NET_ADMIN
            - NET_BIND_SERVICE
      volumeMounts:
        - name: nvidia
          mountPath: /usr/local/nvidia/lib64
        - name: sys
          mountPath: /hostsysfs
        - name: proc-sys
          mountPath: /hostprocsysfs
      env:
        - name: LD_LIBRARY_PATH
          value: /usr/local/nvidia/lib64
    - name: nccl-test
      image: us-docker.pkg.dev/gce-ai-infra/gpudirect-tcpxo/nccl-plugin-gpudirecttcpx-dev:v1.0.3
      imagePullPolicy: Always
      #      securityContext:
      #        privileged: true
      command:
        - /bin/sh
        - -c
        - |
          set -ex
          chmod 755  /scripts/demo-run-nccl-test-tcpxo-via-mpi.sh
          cat >/scripts/allgather.sh <<EOF
          #!/bin/bash
          /scripts/init_ssh.sh \${@};
          pushd /scripts;
          /scripts/gen_hostfiles.sh \${@};
          popd;
          BENCHMARK=all_gather_perf NHOSTS=2 NCCL_LIB_DIR="${LD_LIBRARY_PATH}" LD_LIBRARY_PATH="${LD_LIBRARY_PATH}" /scripts/demo-run-nccl-test-tcpxo-via-mpi.sh
          EOF
          chmod +x /scripts/allgather.sh
          service ssh restart;
          sleep infinity;
      env:
        - name: LD_LIBRARY_PATH
          value: /usr/local/nvidia/lib64
        - name: NCCL_FASTRAK_LLCM_DEVICE_DIRECTORY
          value: /dev/aperture_devices
      volumeMounts:
        - name: nvidia
          mountPath: /usr/local/nvidia/lib64
        - name: shared-memory
          mountPath: /dev/shm
        - name: aperture-devices
          mountPath: /dev/aperture_devices
      resources:
        limits:
          nvidia.com/gpu: 8
  volumes:
    - name: nvidia
      hostPath:
        path: /home/kubernetes/bin/nvidia/lib64
    - name: shared-memory
      emptyDir:
        medium: "Memory"
        sizeLimit: 1Gi
    - name: sys
      hostPath:
        path: /sys
    - name: proc-sys
      hostPath:
        path: /proc/sys
    - name: aperture-devices
      hostPath:
        path: /dev/aperture_devices
```

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-09T07:27:47Z

I believe this behavior (tearing down a node after 10min) is driven by CA rather than Kueue.

@asaiacai what is your CA (and Kube) version? 

Maybe @yaroslava-serdiuk or @mwielgus  would have some suggestions.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-09T08:37:07Z

@asaiacai another thing you might be hitting is maxRunDuration, you can try to update similarly as in this [example](https://github.com/kubernetes-sigs/kueue/blob/7c9ad4c08a5894e654340e03ad338034bbc19279/site/static/examples/provisioning/sample-job.yaml#L9).

Let the community know if this helps. If it doesn't, I would recommend to close the issue here, and open a support ticket for GKE/DWS.

### Comment by [@asaiacai](https://github.com/asaiacai) — 2024-08-09T08:44:29Z

i'm on `1.30.3-gke.1225000` will try changing the run duration.

### Comment by [@asaiacai](https://github.com/asaiacai) — 2024-08-09T10:02:07Z

just updating that bumping the `maxRunDuration` extends the node lifetime. It'd be nice if there was a log or event emitted in the future explaining the pod/node scale down. Closing this issue. Thanks @mimowo !
