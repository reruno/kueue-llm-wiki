# Issue #1834: Copy some labels from Pods/Jobs into the Workload object

**Summary**: Copy some labels from Pods/Jobs into the Workload object

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1834

**Last updated**: 2024-07-10T08:41:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-13T19:48:23Z
- **Updated**: 2024-07-10T08:41:11Z
- **Closed**: 2024-07-10T08:41:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The ability to copy the labels from a Job or Pod (when using pod groups) into the Workload object.

This can be configurable through the configuration API, so that we don't necessarily copy every label.

**Why is this needed**:

This improves the UX for administrators, when trying to list groups of Workloads.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-12T15:11:38Z

It's worth having a mention of this feature in the documentation for Workload.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-15T19:03:49Z

> It's worth having a mention of this feature in the documentation for Workload.

I think that opening this issue would be better to avoid forgetting docs.
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-15T19:03:54Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1834#issuecomment-2057609974):

>> It's worth having a mention of this feature in the documentation for Workload.
>
>I think that opening this issue would be better to avoid forgetting docs.
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-15T19:05:58Z

@pajakd can your write `/assign` in a comment?

### Comment by [@pajakd](https://github.com/pajakd) — 2024-04-16T07:20:05Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:54:03Z

Fixed by #1959

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:54:07Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1834#issuecomment-2189949384):

>Fixed by #1959
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-26T07:40:40Z

@alculquicondor @pajakd Actually, we have never seen documentation for this feature, right?
So, could you add documentation?

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-26T07:40:45Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1834#issuecomment-2191030434):

>@alculquicondor @pajakd Actually, we have never seen documentation for this feature, right?
>So, could you add documentation?
>
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@pajakd](https://github.com/pajakd) — 2024-06-26T07:57:49Z

@tenzen-y I assumed that documentation of field `LabelKeysToCopy` here: https://pkg.go.dev/sigs.k8s.io/kueue@v0.7.0/apis/config/v1beta1#Integrations is sufficient. Should I add something more?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-26T13:42:54Z

Maybe a quick mention in the Workload page.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-08T15:03:43Z

> Maybe a quick mention in the Workload page.

Yes, that is my assumption.
@pajakd Could you open a PR?

### Comment by [@pajakd](https://github.com/pajakd) — 2024-07-09T06:59:13Z

Sure, sorry for the delay: https://github.com/kubernetes-sigs/kueue/pull/2558

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-10T08:41:02Z

resolved by #2558

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-10T08:41:05Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-10T08:41:10Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1834#issuecomment-2219911684):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
