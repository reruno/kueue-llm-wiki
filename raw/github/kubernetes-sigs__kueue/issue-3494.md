# Issue #3494: TAS: pods remain suspended as topology assignment is invalid

**Summary**: TAS: pods remain suspended as topology assignment is invalid

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3494

**Last updated**: 2024-11-13T14:02:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-08T15:00:43Z
- **Updated**: 2024-11-13T14:02:48Z
- **Closed**: 2024-11-13T14:02:48Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

Pods for MPIJob remain suspended



**What you expected to happen**:

The topology assignment is correct for workers, pods get ungated.

**How to reproduce it (as minimally and precisely as possible)**:

I have repro, will share more details later.

based on the yaml
```yaml
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  generateName: pi
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  slotsPerWorker: 1
  runPolicy:
    suspend: true
    cleanPodPolicy: Running
    ttlSecondsAfterFinished: 60
  sshAuthMountPath: /home/mpiuser/.ssh
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-required-topology: "cloud.google.com/gce-topology-host"
        spec:
          containers:
          - image: mpioperator/mpi-pi:openmpi
            name: mpi-launcher
            securityContext:
              runAsUser: 1000
            command:
            - mpirun
            args:
            - -n
            - "2"
            - /home/mpiuser/pi
            resources:
              limits:
                cpu: 1
                memory: 1Gi
    Worker:
      replicas: 40
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-preferred-topology: "cloud.google.com/gce-topology-host"
        spec:
          containers:
          - image: mpioperator/mpi-pi:openmpi
            name: mpi-worker
            securityContext:
              runAsUser: 1000
            command:
            - /usr/sbin/sshd
            args:
            - -De
            - -f
            - /home/mpiuser/.sshd_config
            resources:
              limits:
                cpu: 1
                memory: 4Gi
```

**Anything else we need to know?**:

I see in status:
```yaml
status:
  admission:
    clusterQueue: tas-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        cpu: tas-flavor
        memory: tas-flavor
      name: launcher
      resourceUsage:
        cpu: "1"
        memory: 1Gi
      topologyAssignment:
        domains:
        - count: 1
          values:
          - e2382b4746ceeed246a7dc78750ae29f
          - 9339de12ef53a7fad2d4b45ffadc8ac4
          - a38840ea668bd0baaea716ae16331daa
          - gke-tas-kueue-test-tas-node-pool-47374fa0-0czr
        levels:
        - cloud.google.com/gce-topology-block
        - cloud.google.com/gce-topology-subblock
        - cloud.google.com/gce-topology-host
        - kubernetes.io/hostname
    - count: 40
      flavors:
        cpu: tas-flavor
        memory: tas-flavor
      name: worker
      resourceUsage:
        cpu: "40"
        memory: 160Gi
      topologyAssignment:
        domains: []
        levels:
        - cloud.google.com/gce-topology-block
        - cloud.google.com/gce-topology-subblock
        - cloud.google.com/gce-topology-host
        - kubernetes.io/hostname
```
I have repro, working on fix.

It was reported first here: https://github.com/kubernetes-sigs/kueue/issues/3211#issuecomment-2458900114

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T15:00:49Z

/assign
