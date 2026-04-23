# Issue #9775: Kubeflow 'SparkApplication' integration (Alpha)

**Summary**: Kubeflow 'SparkApplication' integration (Alpha)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9775

**Last updated**: 2026-04-01T10:25:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@everpeace](https://github.com/everpeace)
- **Created**: 2026-03-10T04:19:05Z
- **Updated**: 2026-04-01T10:25:57Z
- **Closed**: 2026-04-01T09:27:48Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**: github.com/kubeflow/spark-operator `SparkApplication` integration support

**Why is this needed**: Spark is one of the most popular batch job framework for scalable data processing. And, kubeflow spark operator's `SparkApplication` is also one of the de-facto ways to run Spark workloads on the kubernetes cluster smoothly.


**Tracking**
- [x] Alpha: v0.17
  - [x] initial integration support: https://github.com/kubernetes-sigs/kueue/pull/7268 (_without_ DRA, ElasticJob, Multikueue)
  - [x] https://github.com/kubernetes-sigs/kueue/pull/9911

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-01T09:27:45Z

Let me follow up with dedicated issues:
- documenation: https://github.com/kubernetes-sigs/kueue/issues/10259
- beta graduation: https://github.com/kubernetes-sigs/kueue/issues/10260
/retitle Kubeflow 'SparkApplication' integration (Alpha)
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-01T09:27:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9775#issuecomment-4168760911):

>Let me follow up with dedicated issues:
>- documenation: https://github.com/kubernetes-sigs/kueue/issues/10259
>- beta graduation: https://github.com/kubernetes-sigs/kueue/issues/10260
>/retitle Kubeflow 'SparkApplication' integration (Alpha)
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
