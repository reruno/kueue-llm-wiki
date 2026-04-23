# Issue #4782: When condition of GPUs is nominalQuota > allocatable, workload admission is not working as expected

**Summary**: When condition of GPUs is nominalQuota > allocatable, workload admission is not working as expected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4782

**Last updated**: 2025-09-11T22:08:41Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ttakahashi21](https://github.com/ttakahashi21)
- **Created**: 2025-03-25T04:00:15Z
- **Updated**: 2025-09-11T22:08:41Z
- **Closed**: 2025-09-11T22:08:40Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When condition of GPUs is nominalQuota > allocatable, Workload Priority Class is not working

**What you expected to happen**:
Low priority jobs are suspended and high priority jobs are executed.

**How to reproduce it (as minimally and precisely as possible)**:


- Condition of GPUs is nominalQuota > allocatable
- Execute two MPI Jobs managed by Kueue
- Set nominalQuota to the number of GPUs that can execute two MPI Jobs
- Attach the number of GPUs that can execute one MPI Job as allocatable GPUs
- Set Priority Class to each Job
- Create dev and prod as Priority Classes and set the priority to be prod > dev.
- Set dev as Priority Class for job1
- Set prod as Priority Class for job2
- Jobs are executed in the order of job1 and job2

The reproduction procedure is as follows.
<details>

1. Create Kind Cluster and set label for fake-gpu-operator
  
   ```bash
   kind create cluster
   kubectl label node kind-control-plane run.ai/simulated-gpu-node-pool=default
   ```

2. Install fake gpu operator
  
   ```bash
   helm repo add fake-gpu-operator https://fake-gpu-operator.storage.googleapis.com
   helm repo update
   helm upgrade -i gpu-operator fake-gpu-operator/fake-gpu-operator --namespace gpu-operator --create-namespace
   ```

- Check that fake gpu is shown by running `kubectl get all -n gpu-operator` and `kubectl describe node | grep "nvidia.com/gpu:"`.
  
3. Install mpi-operator

   ```bash
   kubectl apply --server-side -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v2beta1/mpi-operator.yaml
   ```

- Check that mpi-operator is deployed properly by running `kubectl get all -n mpi-operator`.

4. Install kueue with waitForPodsReady enabled

   Get kueue manifest and enable waitForPodsReady.
   ```bash
   wget https://github.com/kubernetes-sigs/kueue/releases/download/v0.10.2/manifests.yaml
   sed -i '/#waitForPodsReady:/a \    waitForPodsReady:\n      enable: true\n      timeout: 5m\n      blockAdmission: true\n      requeuingStrategy:\n        timestamp: Eviction\n        backoffLimitCount: 5\n        backoffBaseSeconds: 60\n        backoffMaxSeconds: 3600' manifests.yaml
   ```
   Then, apply the configuration by:
   ```bash
   kubectl apply --server-side -f manifests.yaml
   ```

- Check that kueue is deployed properly by running `kubectl get all -n kueue-system`.

5. Prepare minimal kueue setup with gpu enabled

    First, check the amount of allocatable GPU in your cluster. 

    ~~~shell
    TOTAL_ALLOCATABLE=$(kubectl get node --selector='run.ai/simulated-gpu-node-pool=default,node-role.kubernetes.io/control-plane' -o jsonpath='{range .items[*]}{.status.allocatable.nvidia\.com\/gpu}{"\n"}{end}' | numfmt --from=auto | awk '{s+=$1} END {print s}')
    echo $TOTAL_ALLOCATABLE
    ~~~

    In our case this outputs 2.

- Configure ClusterQueue quota and Workload Priority Class

   We configure the GPU flavor by doubling the total GPU allocatable in our cluster, in order to simulate issues with provisioning.

   Execute the following command to create cluster queues configuration as single-clusterqueue-setup-gpu4.yaml:

   ~~~yaml
   cat <<EOF >> single-clusterqueue-setup-gpu4.yaml
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
     preemption:
       withinClusterQueue: LowerPriority
     namespaceSelector: {} # match all.
     resourceGroups:
     - coveredResources: ["nvidia.com/gpu"]
       flavors:
       - name: "default-flavor"
         resources:
         - name: "nvidia.com/gpu"
           nominalQuota: 4 # double the value of allocatable GPU in the cluster
   ---
   apiVersion: kueue.x-k8s.io/v1beta1
   kind: LocalQueue
   metadata:
     namespace: "default"
     name: "user-queue"
   spec:
     clusterQueue: "cluster-queue"
   ---
   apiVersion: kueue.x-k8s.io/v1beta1
   kind: LocalQueue
   metadata:
     namespace: "default"
     name: "user-queue"
   spec:
     clusterQueue: "cluster-queue"
   ---
   apiVersion: kueue.x-k8s.io/v1beta1
   kind: WorkloadPriorityClass
   metadata:
     name: prod-priority
   value: 1000
   description: "Priority class for prod jobs"
   ---
   apiVersion: kueue.x-k8s.io/v1beta1
   kind: WorkloadPriorityClass
   metadata:
     name: dev-priority
   value: 10
   description: "Priority class for development jobs"
   EOF
   ~~~

   Then, apply the configuration by:

   ```bash
   kubectl apply -f single-clusterqueue-setup-gpu4.yaml
   ```

6. Try mpijob works well with 2 replicas (2 gpus are available on the node)

   Get tensorflow-benchmarks.yaml
   ```bash
   wget https://raw.githubusercontent.com/kubeflow/mpi-operator/refs/heads/master/examples/v2beta1/tensorflow-benchmarks/tensorflow-benchmarks.yaml
   ```

7. Run with waitForPodsReady enabled
   
   - Create start.sh script

   ```shell
   cat <<EOF >> start.sh
   sed '/^metadata:/a \  labels:\n    kueue.x-k8s.io/queue-name: user-queue\n    kueue.x-k8s.io/priority-class: dev-priority' tensorflow-benchmarks.yaml | sed  's/name: tensorflow-benchmarks/name: tensorflow-benchmarks-job1/g'  > /tmp/tensorflow-benchmarks-job1.yaml
   sed '/^metadata:/a \  labels:\n    kueue.x-k8s.io/queue-name: user-queue\n    kueue.x-k8s.io/priority-class: prod-priority' tensorflow-benchmarks.yaml | sed  's/name: tensorflow-benchmarks/name: tensorflow-benchmarks-job2/g'  > /tmp/tensorflow-benchmarks-job2.yaml
   kubectl create -f /tmp/tensorflow-benchmarks-job1.yaml
   sleep 10
   kubectl create -f /tmp/tensorflow-benchmarks-job2.yaml
   EOF

   chmod +x start.sh
   ```
   
   - Run the start.sh script

   ```shell
   ./start.sh
   ```

8. Monitor the progress

```bash
   # kubectl get mpijob,workload,pod
NAME                                             AGE
mpijob.kubeflow.org/tensorflow-benchmarks-job1   27s
mpijob.kubeflow.org/tensorflow-benchmarks-job2   17s

NAME                                                              QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/mpijob-tensorflow-benchmarks-job1-c947e   user-queue   cluster-queue   True                  27s
workload.kueue.x-k8s.io/mpijob-tensorflow-benchmarks-job2-c274b   user-queue   cluster-queue   True                  17s

NAME                                            READY   STATUS    RESTARTS   AGE
pod/tensorflow-benchmarks-job1-launcher-cm52h   1/1     Running   0          26s
pod/tensorflow-benchmarks-job1-worker-0         1/1     Running   0          26s
pod/tensorflow-benchmarks-job1-worker-1         1/1     Running   0          26s
pod/tensorflow-benchmarks-job2-launcher-lcld2   1/1     Running   0          16s
pod/tensorflow-benchmarks-job2-worker-0         0/1     Pending   0          16s
pod/tensorflow-benchmarks-job2-worker-1         0/1     Pending   0          16s
```


9. Cleanup

   ```bash
   kubectl delete -f /tmp/tensorflow-benchmarks-job1.yaml
   kubectl delete -f /tmp/tensorflow-benchmarks-job2.yaml
   ```

</details>


**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
Client Version: v1.32.1
Kustomize Version: v5.5.0
Server Version: v1.32.0
- Kueue version (use `git describe --tags --dirty --always`):
0.10.2 
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@ttakahashi21](https://github.com/ttakahashi21) — 2025-03-25T04:24:07Z

@alculquicondor  https://github.com/kubernetes-sigs/kueue/commit/4e3fff436b5342c63361278b79534232d3bf7753
@Gekko0114 https://github.com/kubernetes-sigs/kueue/pull/1081

Is this the behavior you expect as a specification for ClusterQueuePreemption and Workload Priority Class?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-25T13:17:06Z

I'm not sure either of those people are working on Kueue anymore.

@PBundyra would you be able to take a look at this from the `WaitForPodsReady` perspective?

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-03-26T20:38:55Z

@ttakahashi21 This is the expected behavior when nominalQuota exceeds allocatable quota. Kueue admits both workloads and from there it is up to the Kubernetes scheduler. In order to get preemption in this scenario, the nominalQuota for the ClusterQueue must equal the amount which is allocatable and  `.spec.clusterQueuePreemption.withinClusterQueue` would need to set to `"LowerPriority"`

### Comment by [@ttakahashi21](https://github.com/ttakahashi21) — 2025-03-26T21:03:24Z

@KPostOffice I am wondering if we do not have to assume a case where the nominalQuota exceeds the allocatable quota.
I believe this problem occurs when GPUs, etc. are used on resources that are not managed by kueue.
Is the concept of kueue expected to work assuming that the nominalQuota does not exceed the allocatable quota?

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2025-03-27T15:02:12Z

I haven't worked on Kueue these days. Thanks @kannon92 for your quick response :)

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-03-28T19:39:21Z

@ttakahashi21 Kueue can only limit admission based on the nominalQuota defined. In the case where the `total nominalQuota` <= `total allocatable` preemption will work as expected. Kueue can only make preemption decisions at the Workload level based of the resources defined in ClusterQueues. If a resource is not defined in a ClusterQueue's nominalQuota then that resource won't factor into Kueue's scheduling and preemption decisions.

You could use a pods `.spec.priorityClassName` in order to ensure that the Kubernetes Scheduler is able to properly preempt workloads. Is there a reason your ClusterQueues have more quota than the total allocatable?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T19:49:27Z

@ttakahashi21 
If you want to manage computing resources by external systems, you should implement admission-check controllers so that Kueue can recognize the resources. So, in your example, `"nvidia.com/gpu": 2` is managed by Kueue in-tree admission mechanism and `"nvidia.com/gpu": 2` is managed by your admission-check controller for your external resource management system. In this case, you can still specify `"nvidia.com/gpu": 4` in your clusterQueue nominalQuota.

https://kueue.sigs.k8s.io/docs/concepts/admission_check/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T19:50:46Z

/retitle When condition of GPUs is nominalQuota > allocatable, workload admission is not working as expected

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T19:50:56Z

/remove-kind bug
/kind support

### Comment by [@ttakahashi21](https://github.com/ttakahashi21) — 2025-04-07T18:55:31Z

> Is there a reason your ClusterQueues have more quota than the total allocatable?

@KPostOffice I think this problem occurs when GPUs, etc. are used on resources that are not managed by kueue. Or it would also occur when resources are temporarily reduced, such as hardware failure or maintenance.

### Comment by [@ttakahashi21](https://github.com/ttakahashi21) — 2025-04-07T19:01:59Z

@tenzen-y Am I correct in understanding that this can be handled by adding logic in the admission-check controllers?
Perhaps, I think there are cases that cannot be handled by [Provisioning Admission Check Controller](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T20:48:45Z

> Am I correct in understanding that this can be handled by adding logic in the admission-check controllers?

I meant implement AdmissionController by yourself, which controller is not hosted in this upstream repository.
You can implement your own AdmissionController.

> Perhaps, I think there are cases that cannot be handled by [Provisioning Admission Check Controller](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/).

I did not indicate Provisioning Admission Check Controller. I meant the Admission Check Controller. The Provisioning Admission Check Controller is one implementation for the Admission Check Controller.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-13T21:22:40Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-12T22:06:47Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-11T22:08:35Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-11T22:08:41Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4782#issuecomment-3282781105):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
