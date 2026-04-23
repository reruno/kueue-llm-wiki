# Issue #5877: Drop multiple ResourceGroups from ClusterQueue

**Summary**: Drop multiple ResourceGroups from ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5877

**Last updated**: 2025-09-02T10:56:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-04T14:30:56Z
- **Updated**: 2025-09-02T10:56:51Z
- **Closed**: 2025-09-02T10:56:50Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently our API allows technically for multiple ResourceGroups, [here](https://github.com/kubernetes-sigs/kueue/blob/8d20a76a92ad4a4261ded1cb9812360e5bf91349/apis/kueue/v1beta1/clusterqueue_types.go#L65).

However:
- it is not clear what are the use-cases. The documentation says about the licence example, but it is not even clear if this use-case works, because there are no tests for it
- I think the licence use-case could work the same if the `bar.com/license` resource was part of the first ResourceGroup
- it is not supported in TAS at it would result assigning multiple flavors, while TAS checks explicitly onlyFlavor.
- while working with users I've never seen a deployment using multiple ResourceGroups, and I haven't heard any user feedback requesting multiple ResourceGroups.

**Why is this needed**:

To simplify the model of quota management, and the associated code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-04T14:32:45Z

cc @tenzen-y @dgrove-oss @kannon92 @mwysokin @mwielgus @lchrzaszcz @alaypatel07 

Folks, let me know if you have real business use cases for which you use multiple ResourceGroups, and which cannot be solved otherwise. 

If we don't have solid use cases, I would consider adding it to the wishlist of v1beta2.

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-07-04T14:58:59Z

I highly support this idea. I would like to emphasize the simplicity in the code this change would bring if we pursue it, as I am currently experimenting with grouping PodSets together so we can co-locate leader and workers together in LeaderWorkerSet (which entails assigning that to a single flavor because of TAS).

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-05T19:18:42Z

> Folks, let me know if you have real business use cases for which you use multiple ResourceGroups, and which cannot be solved otherwise.

I don't really have a lot of visibilitiy into how end users use the Kueue API at the moment. So this is a difficult question for me to answer.

If we want to deprecate this I think maybe we should announce a deprecation and then drop in v1beta2. I'm not sure when v1beta2 is happening (0.14?) but maybe we could do one release where we log a warning if someone is using multiple ResourceGroups.

We also could send out a email on wg-batch to see if any has usecases for this.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-14T17:53:13Z

@mimowo @tenzen-y  I followed offline with @dgrove-oss and @varshaprasad96 on any known customer use cases for multiple ResourceGroups.

We are not aware of anyone using MultipleResourceGroups but I would still like some kind of deprecation period for a breaking change like this. I am happy with one release with this announcement so we can prepare for it with our release.

With a change like this, I can't imagine a smooth way to generate a conversion webhook so we would need to at least mention a deprecation.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-07-16T19:28:18Z

As the example explains, resource group become useful when some resource are virtual (not associated with any node).
As opposed to resource which are associated with a node such as memory, cpu, any other hardware.

So if will take a look at the example from the docs:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory", "foo.com/gpu"]
    flavors:
    - name: "spot"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
      - name: "foo.com/gpu"
        nominalQuota: 50
    - name: "on-demand"
      resources:
      - name: "cpu"
        nominalQuota: 18
      - name: "memory"
        nominalQuota: 72Gi
      - name: "foo.com/gpu"
        nominalQuota: 100
  - coveredResources: ["bar.com/license"]
    flavors:
    - name: "pool1"
      resources:
      - name: "bar.com/license"
        nominalQuota: 10
    - name: "pool2"
      resources:
      - name: "bar.com/license"
        nominalQuota: 10
```

A workload will reserve its cpu, memory and gpu (all of them) from only one of the flavors - `spot` or `on demand`
For the licences, it can reserve from any of the pools (so there are 20 licences to reserve from).
Without resource groups, the nominal quota for licenses should have been split between the `spot` and `on demand` , but this is not optimal since those licenses don't really consume anything from the nodes the resource flavor represents, so there can be a case where workloads can't use the `spot` flavor even if it has cpu, memory and gpu available but not licenses.

I assume the licences in this example is a software licences, but there are other example such has pool of IPs, pool of cloud resources (buckets, VMs, etc...)

In addition, there is a limit of 16 `coveredResources` per `resourceGroup`, and 16 `resourceGroup` per `ClusterQueue`.
So when it comes to controlling virtual resources, it's possible to control 16*16=256 types.
By dropping resource groups without changing the limitation of 16 `coveredResources` the capacity for controlling different types of virtual resource will drop significantly. 

 My vote is to keep `resourceGroups`

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-07-17T07:02:52Z

As a followup to my previous message, here is a real life example of a clusterQueue which make usage of multiple resources groups. The `platform-group-*` contains nominal quota for VMs allocated on different cloud providers:

```yaml
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cluster-pipeline-queue
spec:
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  stopPolicy: None
  resourceGroups:
  - coveredResources:
    - tekton.dev/pipelineruns
    - cpu
    - memory
    flavors:
    - name: default-flavor
      resources:
      - name: tekton.dev/pipelineruns
        nominalQuota: '500'
      - name: cpu
        nominalQuota: 1k
      - name: memory
        nominalQuota: 500Ti
  - coveredResources:
    - linux-amd64
    - linux-arm64
    - linux-c2xlarge-amd64
    - linux-c2xlarge-arm64
    - linux-c4xlarge-amd64
    - linux-c4xlarge-arm64
    - linux-c6gd2xlarge-arm64
    - linux-c8xlarge-amd64
    - linux-c8xlarge-arm64
    - linux-cxlarge-amd64
    - linux-cxlarge-arm64
    - linux-d160-m2xlarge-amd64
    - linux-d160-m2xlarge-arm64
    - linux-d160-m4xlarge-amd64
    - linux-d160-m4xlarge-arm64
    - linux-d160-m8xlarge-amd64
    flavors:
    - name: platform-group-1
      resources:
      - name: linux-amd64
        nominalQuota: '50'
      - name: linux-arm64
        nominalQuota: '50'
      - name: linux-c2xlarge-amd64
        nominalQuota: '10'
      - name: linux-c2xlarge-arm64
        nominalQuota: '20'
      - name: linux-c4xlarge-amd64
        nominalQuota: '10'
      - name: linux-c4xlarge-arm64
        nominalQuota: '20'
      - name: linux-c6gd2xlarge-arm64
        nominalQuota: '20'
      - name: linux-c8xlarge-amd64
        nominalQuota: '10'
      - name: linux-c8xlarge-arm64
        nominalQuota: '20'
      - name: linux-cxlarge-amd64
        nominalQuota: '10'
      - name: linux-cxlarge-arm64
        nominalQuota: '50'
      - name: linux-d160-m2xlarge-amd64
        nominalQuota: '10'
      - name: linux-d160-m2xlarge-arm64
        nominalQuota: '20'
      - name: linux-d160-m4xlarge-amd64
        nominalQuota: '10'
      - name: linux-d160-m4xlarge-arm64
        nominalQuota: '20'
      - name: linux-d160-m8xlarge-amd64
        nominalQuota: '10'
  - coveredResources:
    - linux-d160-m8xlarge-arm64
    - linux-extra-fast-amd64
    - linux-fast-amd64
    - linux-g6xlarge-amd64
    - linux-m2xlarge-amd64
    - linux-m2xlarge-arm64
    - linux-m4xlarge-amd64
    - linux-m4xlarge-arm64
    - linux-m8xlarge-amd64
    - linux-m8xlarge-arm64
    - linux-mlarge-amd64
    - linux-mlarge-arm64
    - linux-mxlarge-amd64
    - linux-mxlarge-arm64
    - linux-ppc64le
    - linux-root-amd64
    flavors:
    - name: platform-group-2
      resources:
      - name: linux-d160-m8xlarge-arm64
        nominalQuota: '20'
      - name: linux-extra-fast-amd64
        nominalQuota: '10'
      - name: linux-fast-amd64
        nominalQuota: '10'
      - name: linux-g6xlarge-amd64
        nominalQuota: '10'
      - name: linux-m2xlarge-amd64
        nominalQuota: '10'
      - name: linux-m2xlarge-arm64
        nominalQuota: '20'
      - name: linux-m4xlarge-amd64
        nominalQuota: '10'
      - name: linux-m4xlarge-arm64
        nominalQuota: '20'
      - name: linux-m8xlarge-amd64
        nominalQuota: '10'
      - name: linux-m8xlarge-arm64
        nominalQuota: '20'
      - name: linux-mlarge-amd64
        nominalQuota: '10'
      - name: linux-mlarge-arm64
        nominalQuota: '50'
      - name: linux-mxlarge-amd64
        nominalQuota: '10'
      - name: linux-mxlarge-arm64
        nominalQuota: '20'
      - name: linux-ppc64le
        nominalQuota: '64'
      - name: linux-root-amd64
        nominalQuota: '10'
  - coveredResources:
    - linux-root-arm64
    - linux-s390x
    flavors:
    - name: platform-group-3
      resources:
      - name: linux-root-arm64
        nominalQuota: '50'
      - name: linux-s390x
        nominalQuota: '60'
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T07:20:22Z

@gbenhaim thank you for the insights!

> A workload will reserve its cpu, memory and gpu (all of them) from only one of the flavors - spot or on demand
For the licences, it can reserve from any of the pools (so there are 20 licences to reserve from).
Without resource groups, the nominal quota for licenses should have been split between the spot and on demand , but this is not optimal since those licenses don't really consume anything from the nodes the resource flavor represents, so there can be a case where workloads can't use the spot flavor even if it has cpu, memory and gpu available but not licenses.

Great explanation, would you mind expanding the comment in this [example](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#resource-groups)

> In addition, there is a limit of 16 coveredResources per resourceGroup, and 16 resourceGroup per ClusterQueue.
So when it comes to controlling virtual resources, it's possible to control 16*16=256 types.
By dropping resource groups without changing the limitation of 16 coveredResources the capacity for controlling different types of virtual resource will drop significantly.

Yeah, but this alone sounds more like a hack. If you have use-cases for using more than 16 resources, I would rather expand the size rather than require splitting them artificially into groups. 

Note that we could still cap the total number of resources at 256, but just reformulate the check - not constrain the size of the list of resources per group as 16, but total number of resources.

wdyt @gbenhaim @tenzen-y ?

> As a followup to my previous message, here is a real life example of a clusterQueue which make usage of multiple resources groups. The platform-group-* contains nominal quota for VMs allocated on different cloud providers:

Thank you, the example makes sense, but in this example, if you had the limit 256 instead of 16, then you wouldn't need to use multiple resource-groups, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T07:34:36Z

fyi: https://github.com/kubernetes-sigs/kueue/issues/6007

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-07-17T07:36:16Z

> Great explanation, would you mind expanding the comment in this [example](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#resource-groups)

sure thing.

> Thank you, the example makes sense, but in this example, if you had the limit 256 instead of 16, then you wouldn't need to use multiple resource-groups, right?

Yes correct. If I would add another flavor to the first resource group than it would also fit the [first use case I described above.](https://github.com/kubernetes-sigs/kueue/issues/5877#issuecomment-3082905286)

> Note that we could still cap the total number of resources at 256, but just reformulate the check - not constrain the size of the list of resources per group as 16, but total number of resources.
> 
> wdyt @gbenhaim @tenzen-y ?

I think that without relation to the removal of resource group this is a great suggestion https://github.com/kubernetes-sigs/kueue/issues/6007

With that being said, I still think resource groups can be useful as I mentioned above.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T08:09:11Z

> With that being said, I still think resource groups can be useful as I mentioned above.

Thank you for the vote, and supporting it with the examples. The licenses examples is good, but requires a bit more of clarifying . For example, we could simplify it by only having one license flavor (pool instead of pool1 and pool2). Making the example minimal will make it easier to undestand imo.

I opened the issue specifically to hear the community use-cases, as it complicates the code significantly, and requires substantial additional testing (which I think we are currently lacking, even if it works).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T10:43:10Z

I just realized there is another neat use-case for multiple ResourceGroups based on ConfigurableResourceTransformations. 

Assume a system has 2 flavors (for simplicity using CPU) and the admin wants to limit the total usage of the CPU per team, independently if using flavor1 or flavor2.

In this example we use virtual "cpu_credits" to represent the joint quota, ptal:

ConfigMap
```yaml
resources:
  transformations:
  - input: cpu
    strategy: Retain
    outputs:
      cpu_credits: 1
```

Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["300s"]
        resources:
          requests:
            cpu: "1"
      restartPolicy: Never
```

ClusterQueues:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "flavor1"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "flavor2"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "credits"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "flavor1"
      resources:
      - name: "cpu"
        nominalQuota: 9
    - name: "flavor2"
      resources:
      - name: "cpu"
        nominalQuota: 9
  - coveredResources: ["cpu_credits"]
    flavors:
    - name: "credits"
      resources:
      - name: cpu_credits
        nominalQuota: 14
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```
Then, after creating 5 jobs we can see only 4 is running:

```sh
> k get wl               
NAME                        QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
job-sample-job5xrvk-49ed1   user-queue   cluster-queue   True                  3s
job-sample-job6stmt-35fb7   user-queue   cluster-queue   True                  2s
job-sample-jobgbslx-e9260   user-queue   cluster-queue   True                  3s
job-sample-jobhklf7-55c33   user-queue                                         2s
job-sample-jobnq2b4-98531   user-queue   cluster-queue   True                  4s
```
because the 5th is limited by cpu_credits:
```sh
> k describe wl job-sample-jobhklf7-55c33 | tail
    Type:                  QuotaReserved
  Resource Requests:
    Name:  main
    Resources:
      Cpu:          3
      cpu_credits:  3
Events:
  Type     Reason   Age   From             Message
  ----     ------   ----  ----             -------
  Warning  Pending  68s   kueue-admission  couldn't assign flavors to pod set main: insufficient unused quota for cpu_credits in flavor credits, 1 more needed
```

I think it would be quite helpful to document this use-case scenario, unless I'm missing something. wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T10:56:46Z

/close 
As discussed there are reasons to keep this offering. 
I opened a dedicated issue to document the use case mentioned in the previous comment: https://github.com/kubernetes-sigs/kueue/issues/6704

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-02T10:56:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5877#issuecomment-3244829331):

>/close 
>As discussed there are reasons to keep this offering. 
>I opened a dedicated issue to document the use case mentioned in the previous comment: https://github.com/kubernetes-sigs/kueue/issues/6704


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
