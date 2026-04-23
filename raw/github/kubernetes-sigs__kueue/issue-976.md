# Issue #976: Managing raw pods

**Summary**: Managing raw pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/976

**Last updated**: 2024-01-26T17:50:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-07-11T17:35:28Z
- **Updated**: 2024-01-26T17:50:19Z
- **Closed**: 2024-01-26T17:50:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@achernevskii](https://github.com/achernevskii)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Management of raw pods. 

kube-scheduler added support for a feature named scheduling gates, which allows an external controller to control when kube-scheduler should consider the pod for scheduling, so in a sense providing pod-level pause capability. This can be used by Kueue to manage raw pods.

**Why is this needed**:
Some workloads are better managed at the pod level, like Spark. This will also make it easier to support any job type without explicit integration.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T17:52:48Z

/assign

I want to take a stab at the design first.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-18T16:51:39Z

Also related to #77

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-05T11:20:05Z

@alculquicondor @achernevskii Do we try to implement all features designed in KEP by release v0.5?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-05T15:43:17Z

No, we'll just go with single pod support in 0.5 and follow up on 0.6 with the rest.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-05T17:38:27Z

> No, we'll just go with single pod support in 0.5 and follow up on 0.6 with the rest.

SGTM
I was concerned that this feature blocks the v0.5 release.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-23T08:24:12Z

I guess this is completed, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-23T08:29:55Z

> I guess this is completed, right?

This is not completed. The kueue doesn't support https://github.com/kubernetes-sigs/kueue/blob/main/keps/976-plain-pods/README.md#groups-of-pods-created-beforehand yet.

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-11T14:21:39Z

/assign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-05T10:31:05Z

One potential issue here is pod is both watched by kueue and scheduler, and scheduler may complete the scheduling cycle in prior than kueue, then patching gates to pod will be failed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-05T10:40:54Z

> One potential issue here is pod is both watched by kueue and scheduler, and scheduler may complete the scheduling cycle in prior than kueue, then patching gates to pod will be failed.

@kerthcet IIUC, there isn't such a potential issue since the webhook will work before the kube-scheduler will do anything to the pod, right?

https://github.com/kubernetes-sigs/kueue/blob/1579d75e5a35bdb4ab24c64b2da4e4effa98bbc8/pkg/controller/jobs/pod/pod_webhook.go#L186

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-05T15:54:52Z

Keep in mind that it's not possible to add scheduling gates to an existing pod. They always have to be set on creation or by webhooks.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-07T06:40:46Z

> there isn't such a potential issue since the webhook will work before the kube-scheduler will do anything to the pod

Yes, I found it, I'm in an environment with kubernetes 1.24 which doesn't support scheduling gates. sorry for that.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T17:50:13Z

/close

Splitting remaining use case into a different issue: https://github.com/kubernetes-sigs/kueue/issues/1656

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-26T17:50:18Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/976#issuecomment-1912451824):

>/close
>
>Splitting remaining use case into a different issue: https://github.com/kubernetes-sigs/kueue/issues/1656


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
