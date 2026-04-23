# Issue #2076: Command line tool for clusterqueue/localqueue/workload listing and management

**Summary**: Command line tool for clusterqueue/localqueue/workload listing and management

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2076

**Last updated**: 2024-06-17T18:38:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-04-26T08:57:43Z
- **Updated**: 2024-06-17T18:38:55Z
- **Closed**: 2024-06-17T18:38:54Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**:

A tool (for example a kubectl plugin) to perform listing and management operations on Kueue objects. 

**Why is this needed**:

Many common operations (like listing pending workloads from a particular cluster queue, draining a queue, pausing workload admission, moving workloads between queues) require advanced API knowledge and are inconvenient to execute using kubectl. 

#487 covers only listing, we need a broader tool.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T18:41:42Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-01T18:41:46Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2076#issuecomment-2088905722):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-02T08:48:50Z

- [x] #2112
- [x] #2113
- [x] #2115
- [x] #2114
- [x] #2135 
- [x] #2132
- [x] #2133
- [x] #2136 
- [x] #2137 
- [x] #2139
- [x] #2138 
- [x] #2180
- [x] #2183
- [x] #2313
- [x] #2314
- [x] #2346

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T18:38:50Z

/close

All tasks are completed

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-17T18:38:54Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2076#issuecomment-2174170032):

>/close
>
>All tasks are completed


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
