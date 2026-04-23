# Issue #112: Custom Job only queue

**Summary**: Custom Job only queue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/112

**Last updated**: 2022-04-04T10:59:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-03-10T18:19:51Z
- **Updated**: 2022-04-04T10:59:19Z
- **Closed**: 2022-04-04T10:59:18Z
- **Labels**: `kind/feature`, `priority/awaiting-more-evidence`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
In line with #65 #77 ,  once we define a clear path for supporting custom jobs, plugin or framework like.
We could consider blocking queues to only accept a specific type of job/workload

**Why is this needed**:

As a system Admin I would like to create/curate a custom job for my organization, and block users from queuing workloads outside of the "supported" framework.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T19:02:12Z

/priority longterm

can you expand on why they admins would care about the specific API? Usually they just care about what resources they consume.

Also, to create MPIJob (for example) you need to add the permission to create such objects to a Role. Isn't that enough?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-10T19:02:13Z

@alculquicondor: The label(s) `priority/longterm` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/112#issuecomment-1064393462):

>/priority longterm
>
>can you expand on why they admins would care about the specific API? Usually they just care about what resources they consume.
>
>Also, to create MPIJob (for example) you need to add the permission to create such objects to a Role. Isn't that enough?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T19:06:22Z

> /priority longterm
> 
> can you expand on why they admins would care about the specific API? Usually they just care about what resources they consume.
> 
> Also, to create MPIJob (for example) you need to add the permission to create such objects to a Role. Isn't that enough?

Sure.

I am not thinking from a security point of view, more like a custom resource utilization scenario + custom job. Someone could want to block a Queue for specific purposes, bc they will track that Queue on Prometheus as example.

I agree this is long term, I just had the idea and wanted to leave record of it. Maybe I am out of coffee but sounds like a good scenario to isolate Queues for specific purposes.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T19:10:11Z

/priority awaiting-more-evidence

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-04T01:38:36Z

> but sounds like a good scenario to isolate Queues for specific purposes.

This is discussed in the initial proposal. Apart from basic support for namespace selector in ClusterQueue (basic tenancy control), admins can use policy controllers like GateKeeper to implement more advanced scenarios.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-04T10:59:08Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-04T10:59:19Z

@ArangoGutierrez: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/112#issuecomment-1087410572):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
