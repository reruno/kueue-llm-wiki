# Issue #45: Add scalability tests

**Summary**: Add scalability tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/45

**Last updated**: 2022-12-21T15:42:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-22T02:44:05Z
- **Updated**: 2022-12-21T15:42:58Z
- **Closed**: 2022-12-21T15:42:57Z
- **Labels**: `help wanted`, `priority/important-longterm`, `lifecycle/frozen`, `kind/productionization`
- **Assignees**: _none_
- **Comments**: 15

## Description

This is critical to better understand kueue's limits and where its bottlenecks. We should check if there is a way to use clusterloader for this

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-09T01:25:37Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-09T01:25:38Z

@ahg-g: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/45):

>/help 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:29:29Z

I think the first we can do for this issue is to lay down what we want to test/bench for Kueue.
I think I good first approach is to get a baseline of resource utilization vs scale.

- [ ] How many sample queues can kueue hold when running on 1 cpu and 200MB mem. 
- [ ] On an empty cluster with "infinite" resources, how long does it take to Kueue to fully `admit` all the jobs into a ClusterQueue

those are init test ideas

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-15T15:35:58Z

I think we should test "infinite" resources but also "limited" (say, the ClusterQueues have 20% of the total required requests for all jobs)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T20:29:06Z

With config 
```bash
tuned-adm profile virtual-host
minikube start \
        --driver=kvm2 --container-runtime=cri-o \
        --extra-config=kubelet.cgroup-driver=systemd \
        --kubernetes-version=latest \
        --kvm-numa-count=1 \
        --nodes=3 --cpus=3 --memory=4g \
```

10 jobs CPU/Mem usage:
![Screenshot from 2022-03-15 16-27-00](https://user-images.githubusercontent.com/15933089/158466446-a94181eb-12cc-49f5-9a04-2c39243eeb85.png)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T21:13:24Z

Can't get more on Minikube :( , will have to move to something else. will report more later

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T23:34:45Z

empty queues, staging Kueue, after 15 mins of inactivity  (bootstrap stabilization) 

> Base line

![Screenshot from 2022-03-15 19-33-30](https://user-images.githubusercontent.com/15933089/158489160-c043e7ae-e9e7-439a-98e4-f4d1ff4a919e.png)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-12T21:03:46Z

We need to create a list of target features to stress test to move forward with this issue

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-12T21:05:51Z

Do we want to do resource utilization testing? 
e.g :
- How many CPU and MEM is used by Kueue while processing X number of Workloads
- CPU and MEM on a system with "infinite" resources vs a system with no resources, to see how a high traffic moment can affect resource consumption by Kueue.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-12T21:06:39Z

- In a system with "infinite" resources, how long does it take to Queue to *admit* X number of workloads

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T02:53:17Z

We need to run tests that measure:
1. Workload admission latency
2. Workload admission throughput
3. cpu/memory (we don't set the limits, so it can compete with whatever available resources on the master)

The scale test should measure that while varying 
1. The number of Namespaces/Queues; tens to hundreds.
1. The number of ClusterQueues; few to as many as Namespaces
4. The number workloads; hundreds, thousands, to few tens of thousands

As for CPU and memory requests, we can use settings similar to kube-scheduler.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T03:12:11Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T13:15:12Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T15:42:53Z

A first load test was added in #462.

We can create separate issues for follow ups and to improve performance.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-21T15:42:57Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/45#issuecomment-1361524237):

>A first load test was added in #462.
>
>We can create separate issues for follow ups and to improve performance.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
