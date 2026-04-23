# Issue #746: Count insufficient resources as borrowed resources in ClusterQueue that has no cohort

**Summary**: Count insufficient resources as borrowed resources in ClusterQueue that has no cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/746

**Last updated**: 2023-05-10T19:11:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-05-05T18:37:57Z
- **Updated**: 2023-05-10T19:11:01Z
- **Closed**: 2023-05-10T19:11:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Once we change the `nominalQuota` in ClusterQueue by less than the quotas consumed by the running pods, the kueue controller counts insufficient resources as borrowed resources from the cohort in ClusterQueue even if that ClusterQueue doesn't belong any cohort.

```yaml
...
status:
  admittedWorkloads: 1
  flavorsUsage:
  - name: default-flavor
    resources:
    - borrowed: "2"
      name: cpu
      total: "3"
    - borrowed: "0"
      name: memory
      total: 600Mi
...
```

**What you expected to happen**:
The insufficient resources aren't counted as borrowed resources.

**How to reproduce it (as minimally and precisely as possible)**:

1. Set up single clusterqueue:

```shell
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/config/samples/single-clusterqueue-setup.yaml
```

2. Deploy sample Jobs:

```shell
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/config/samples/sample-job.yaml
```

3. Confirm that jobs are admitted by ClusterQueue:

```shell
$ kubectl get workloads -n default
NAME                         QUEUE        ADMITTED BY     AGE
job-sample-job-2sssv-53569   user-queue   cluster-queue   5s
```

4. Update ClusterQueue with insufficient nominalQuota:

```shell
$ kubectl patch clusterqueues cluster-queue --type json -p '[{"op": "replace", "path": "/spec/resourceGroups/0/flavors/0/resources/0/nominalQuota", "value":"1"}]'
```

5. Show the Status of ClusterQueue:

```shell
$ kubectl get clusterqueues.kueue.x-k8s.io cluster-queue -ojsonpath='{.status.flavorsUsage}' | jq .

# You will get the below response:
# [
#   {
#     "name": "default-flavor",
#     "resources": [
#       {
#         "borrowed": "2",
#         "name": "cpu",
#         "total": "3"
#       },
#       {
#         "borrowed": "0",
#         "name": "memory",
#         "total": "600Mi"
#       }
#     ]
#   }
# ]
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.4
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration: kind cluster
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-05T18:48:15Z

We may need to consider how to handle such situations.

Maybe, if we block the downscale in ClusterQueue, as mentioned in #314, we can avoid such situations.

If we don't block the downscale, we may be able to take the below options:

1. Add a new field `dangling` to `.status.flavorsUsage.resources` in ClusterQueue.
2. Allow a negative value in `.status.flavorsUsage.resources.borrowed` in ClusterQueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-05T18:48:34Z

@alculquicondor What do you think?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-05T19:31:32Z

In theory, this would be a transitory period while the jobs terminate, so I wouldn't add a field just for this.

In the case where the CQ doesn't belong to a cohort, the answer is simple: this CQ is not borrowing, it's just over-committed. So we should set borrowing as zero.

In the case where the CQ belongs to a cohort, I would argue that the CQ is now borrowing, even if there aren't enough resources in the cohort (then, the cohort is over-committed). But considering that this CQ is borrowing is useful, because other CQs in the cohort might be able to preempt workloads from it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-05T19:38:43Z

> In theory, this would be a transitory period while the jobs terminate, so I wouldn't add a field just for this.
> 
> In the case where the CQ doesn't belong to a cohort, the answer is simple: this CQ is not borrowing, it's just over-committed. So we should set borrowing as zero.
> 
> In the case where the CQ belongs to a cohort, I would argue that the CQ is now borrowing, even if there aren't enough resources in the cohort (then, the cohort is over-committed). But considering that this CQ is borrowing is useful, because other CQs in the cohort might be able to preempt workloads from it.

That makes sense.
I'll fix it so that we can set borrowing as zero if the clusterQueue doesn't belong to a cohort.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-05T19:39:16Z

/assign
