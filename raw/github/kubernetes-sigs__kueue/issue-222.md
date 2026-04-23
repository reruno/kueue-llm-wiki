# Issue #222: [Umbrella] ☂️ Requirements for release 0.2.0

**Summary**: [Umbrella] ☂️ Requirements for release 0.2.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/222

**Last updated**: 2022-08-25T21:06:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-04-15T14:38:25Z
- **Updated**: 2022-08-25T21:06:56Z
- **Closed**: 2022-08-25T21:06:55Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 21

## Description

Issues that we need to complete to consider Kueue ready for the second release:

I suggest to focus only on issues related to [Productionisation](https://github.com/kubernetes-sigs/kueue/issues?q=is%3Aissue+is%3Aopen+label%3Akind%2Fproductionization):
- [x] [Knobs to configure which jobs Kueue manages](https://github.com/kubernetes-sigs/kueue/issues/169) 
- [x] [More detailed pending event](https://github.com/kubernetes-sigs/kueue/issues/189)
- [x] [Handle Pod overhead added during pod admission](https://github.com/kubernetes-sigs/kueue/issues/119)
- [x] [Add "Frozen" ClusterQueue state](https://github.com/kubernetes-sigs/kueue/issues/134)
- [x] [Rename image to registry.k8s.io/kueue/kueue](https://github.com/kubernetes-sigs/kueue/issues/226)
- [x] [Manage webhook cert internally](https://github.com/kubernetes-sigs/kueue/issues/232)
- [x] [Trigger the movement of workload in ClusterQueue by ns event](https://github.com/kubernetes-sigs/kueue/issues/234)
- [x] [Add webhook for APIs defaulting and validation](https://github.com/kubernetes-sigs/kueue/issues/171)
  - #308
- [x] [Add ClusterQueue and Queue Metrics](https://github.com/kubernetes-sigs/kueue/issues/199)
  - #324
- [x] [Using the same flavors in different resources might lead to unschedulable pods](https://github.com/kubernetes-sigs/kueue/issues/167) 
- [x] [Avoid queueing workloads that don't match CQ namespaceSelector](https://github.com/kubernetes-sigs/kueue/issues/301)
- [x] [Should we use server-side apply for admission?](https://github.com/kubernetes-sigs/kueue/issues/164)
- [x] [Rename the namespaced resource "Queue" ](https://github.com/kubernetes-sigs/kueue/issues/330)
- [x] Update docs


Nice to have:
- [ ] [Add real E2E test setup and first test](https://github.com/kubernetes-sigs/kueue/issues/61)
- [ ] [Add scalability tests](https://github.com/kubernetes-sigs/kueue/issues/45)

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-15T14:41:57Z

Our backlog of features is listed below, but I think we shouldn't add any more features before closing our backlog of productionization/hardening related issues:
- [Support Spark jobs specifically and dynamically sized jobs](https://github.com/kubernetes-sigs/kueue/issues/77)
- [Support kubeflow's MPIJob](https://github.com/kubernetes-sigs/kueue/issues/65)
- [Replace borrowing ceiling with weights](https://github.com/kubernetes-sigs/kueue/issues/62)
- [Workload preemption](https://github.com/kubernetes-sigs/kueue/issues/83)
- [Simple Framework to support different queuing policies](https://github.com/kubernetes-sigs/kueue/issues/10)
- [Budgets](https://github.com/kubernetes-sigs/kueue/issues/28)
- [Hierarchical ClusterQueues](https://github.com/kubernetes-sigs/kueue/issues/79)
- [Include ClusterQueue depth in Workload status](https://github.com/kubernetes-sigs/kueue/issues/168)


@alculquicondor @denkensk @ArangoGutierrez @kerthcet what do you think?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-15T14:49:45Z

Glad to see a backlog here, do we have a rough deadline?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-18T03:55:34Z

> Our backlog of features is listed below, but I think we shouldn't add any more features before closing our backlog of productionization/hardening related issues.

sgtm.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-19T12:45:48Z

lgtm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-19T14:43:13Z

+1

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-20T15:02:05Z

#226 to be good k8s citizens :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-26T17:53:45Z

#232 to simplify deployment of webhooks

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-07T09:14:41Z

Should we set a deadline as @kerthcet suggested? Perhaps after KubeCon?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-09T16:53:15Z

I think we still have a lot to solve, so I wouldn't bet on a release within a week of Kubecon. Maybe June 15th for the batch live panel? https://opensourcelive.withgoogle.com/learn-kubernetes

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-05-09T19:45:56Z

226 is closed now :)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-10T03:37:36Z

Maybe we can release regularly to avoid similar discussion later. Features are always there.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-13T15:32:52Z

FYI
@ahg-g and I will be in kubecon next week (May 16th), so we might have limited time to approve PRs.
The week after, we are both out on vacation (May 23th).
I'll be back in May 30th.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-05-13T15:39:15Z

@ahg-g  @alculquicondor  Have a nice vacation! 
I could probably spend more time fixing some urgent issues and reviewing code.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-13T23:49:26Z

Have a wonderful speech 🚀, and I'll help on reviewing the same time.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-15T13:50:35Z

consider adding https://github.com/kubernetes-sigs/kueue/issues/103 to this release as well

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-20T10:09:11Z

> consider adding #103 to this release as well

I'm already in settling the deletion part of the work.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T07:54:01Z

What is left for v0.2.0, it seems the necessary ones are all finished.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-19T13:31:39Z

#341, update API version to v1alpha2, and update documentation

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T17:17:52Z

Started the release checklist in #352

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-25T21:06:44Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-25T21:06:55Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/222#issuecomment-1227762948):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
