# Issue #697: QueueName in Workload sometimes is removed

**Summary**: QueueName in Workload sometimes is removed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/697

**Last updated**: 2023-05-03T12:01:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-04-14T20:36:53Z
- **Updated**: 2023-05-03T12:01:59Z
- **Closed**: 2023-05-03T12:01:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
After I deployed two MPIJobs and the kueue-controller created Workload with QueueName, the kueue-controller sometimes removes `.spec.queueName` in Workload.

```shell
$ kubectl get workloads.kueue.x-k8s.io 
NAME                QUEUE        ADMITTED BY     AGE
mpijob-pi-0-1881b   user-queue   cluster-queue   54s
mpijob-pi-1-ef222   user-queue                   54s
$
$ kubectl get workloads.kueue.x-k8s.io 
NAME                QUEUE        ADMITTED BY     AGE
mpijob-pi-0-1881b   user-queue   cluster-queue   55s
mpijob-pi-1-ef222                                55s
```

**What you expected to happen**:
QueueName in Workload isn't removed.

**How to reproduce it (as minimally and precisely as possible)**:

- manifests for kueue

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 4
      - name: "memory"
        nominalQuota: 5Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```

- MPIJobs

```yaml
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: pi-0
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
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
      replicas: 2
      template:
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
                memory: 1Gi
---
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: pi-1
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
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
      replicas: 2
      template:
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
                memory: 1Gi
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.5
- Kueue version (use `git describe --tags --dirty --always`): v0.4.0
- Cloud provider or hardware configuration: On-Prem
- OS (e.g: `cat /etc/os-release`): 
```
NAME="Ubuntu"
VERSION="20.04.5 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.5 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```
- Kernel (e.g. `uname -a`): `Linux 5.4.0-136-generic #153-Ubuntu SMP Thu Nov 24 15:56:58 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux`
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-14T20:37:22Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-14T22:41:03Z

Please include a change for the changelog when you work on the fix. You probably need to create a new file for 0.4. Once approved we can cherry pick.
Thanks for reporting!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-17T12:22:57Z

> Please include a change for the changelog when you work on the fix. You probably need to create a new file for 0.4. Once approved we can cherry pick. Thanks for reporting!

Sure!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-22T20:23:51Z

Through more investigation, the below process updates the queue name with an empty:

https://github.com/kubernetes-sigs/kueue/blob/9ca57c86cf06c11a94a2d5b7badf60233a51a2f2/pkg/controller/jobframework/reconciler.go#L181-L191

When I commented on the above place, the queue name wasn't updated with an empty.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-22T21:07:27Z

Oh, I could reach the root cause :)
It seems that the batch/v1 Job integration controller updates the field.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-24T18:36:22Z

Was there something putting the queue name back? Or is the MPIJob permanently stuck?
Depending on the answer, we might want to release 0.3.1 with just this fix.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-24T18:44:55Z

> Was there something putting the queue name back? Or is the MPIJob permanently stuck? Depending on the answer, we might want to release 0.3.1 with just this fix.

The kueue-controller puts the queue name on the workload again. So MPIJob wasn't permanently stuck.

The queue name in the workload continues to be updated infinitely :) 

empty value -> appropriate queue name -> empty value -> appropriate queue name -> ...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-24T19:36:01Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-24T19:36:05Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/697#issuecomment-1520721233):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-24T19:44:12Z

IMO, I'd like to cut a patch release since if we deploy many MPIJobs, the number of reconciling probably will explode :(

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T14:10:11Z

Uhm... how about after we fix #704?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-25T15:42:34Z

> Uhm... how about after we fix #704?

I'm ok with cutting a patch release after #704 is fixed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T12:01:11Z

The cherry-pick #729 is merged

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T12:01:54Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-03T12:01:58Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/697#issuecomment-1532902786):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
