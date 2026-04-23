# Issue #4433: Securing APIService for Visibility Feature

**Summary**: Securing APIService for Visibility Feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4433

**Last updated**: 2025-09-23T13:13:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-27T14:50:59Z
- **Updated**: 2025-09-23T13:13:51Z
- **Closed**: 2025-09-23T13:13:50Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
https://github.com/kubernetes-sigs/kueue/blob/main/config/components/visibility/apiservice_v1beta1.yaml

APIService skips TLS checks so we will not enable this feature for our cluster.

Kueue should provide support for securing this service using certificates.

**Why is this needed**:

For my organization, any endpoint not guarded by TLS or using insecure options is flagged as a potential security vulnerability. Since this is an optional feature we are not deploying this in our Kueue instalation. It would be a good feature to have.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-28T15:16:58Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T11:11:08Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-24T12:09:10Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-24T12:09:12Z

@kannon92: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4433):

>/help
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-08-25T19:01:56Z

/assign

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-08-25T19:02:39Z

I would like to help with this issue if it's fine by everyone.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T01:57:23Z

> I would like to help with this issue if it's fine by everyone.

+1

Thank you for your help!

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-08-28T13:47:47Z

@kannon92 hello,
would you say that the following would be the requirements for this issue?

- Generate the certificate like it's done for other services https://github.com/openshift/kubernetes-sigs-kueue/blob/main/config/components/certmanager/certificate-metrics.yaml
-  Adapt `controller-manager` manifest to include the new certificate that exist in a secret as a volume
- Adapt `APIService` to include [caBundle](https://issues.redhat.com/browse/OCPNODE-3624#apiservice-apiregistration-k8s-io-v1) from the certificate generated in the secret https://cert-manager.io/docs/concepts/ca-injector/
- Adapt helm related charts

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-28T13:49:58Z

That sounds like a good plan.

@tenzen-y @mimowo should we include e2e test relying on Cert Manager for this also?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-28T13:50:28Z

I would also add a bullet point for Helm related charts also.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T13:13:45Z

This was reached by https://github.com/kubernetes-sigs/kueue/pull/6798
@MaysaMacedo Thanks!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-23T13:13:51Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4433#issuecomment-3323968233):

>This was reached by https://github.com/kubernetes-sigs/kueue/pull/6798
>@MaysaMacedo Thanks!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
