# Issue #270: Make internal cert parameters configurable via component config

**Summary**: Make internal cert parameters configurable via component config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/270

**Last updated**: 2022-09-09T16:35:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-06-07T06:58:03Z
- **Updated**: 2022-09-09T16:35:21Z
- **Closed**: 2022-09-09T14:47:25Z
- **Labels**: `kind/feature`, `help wanted`, `priority/important-longterm`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Make parameters configurable

**Why is this needed**:
refer to https://github.com/kubernetes-sigs/kueue/pull/265/files#r890449020
**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T20:57:33Z

I'm ok leaving this for 0.3.0 if you don't have time for this @kerthcet

Otherwise, we can open it up to other contributors?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-12T08:52:26Z

Yes, I didn't assign to myself. 
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-12T08:52:27Z

@kerthcet: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/270):

>Yes, I didn't assign to myself. 
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-12T08:53:16Z

/priority important-longterm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-08-28T17:38:40Z

@kerthcet @alculquicondor Hi.
I'm interested in this issue. Can I take this?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-29T00:40:09Z

> @kerthcet @alculquicondor Hi.
> 
> I'm interested in this issue. Can I take this?
> 
> 

Thanks, plz go ahead.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-08-29T01:36:36Z

@kerthcet Thanks for your response.
I think that we can extend the `config.kueue.x-k8s.io` API such as the following patterns:

- A

```diff
type Configuration struct {
...
    EnableInternalCertManagement *bool `json:"enableInternalCertManagement,omitempty"`

+   InternalCertManagementServiceName string `json:"internalCertManagementServiceName"`

+   InternalCertManagementSecretName string `json:"internalCertManagementSecretName"`
}
```
- B

```diff
type Configuration struct {
...
    EnableInternalCertManagement *bool `json:"enableInternalCertManagement,omitempty"`

+   InternalCertManagementConfig InternalCertManagementConfig `json:"internalCertManagementConfig"`
}

+type InternalCertManagementConfig struct {
+    ServiceName string `json:"internalCertManagementServiceName"`

+    SecretName string `json:"internalCertManagementSecretName"`
}
```

- C

```diff
type Configuration struct {
...
-   EnableInternalCertManagement *bool `json:"enableInternalCertManagement,omitempty"`

+   InternalCertManagement InternalCertManagement `json:"internalCertManagement"`
}

+type InternalCertManagement struct {
+   Enable *bool `json:"enable"`

+   ServiceName string `json:"internalCertManagementServiceName"`

+   SecretName string `json:"internalCertManagementSecretName"`
}
```

What do you assume API structure?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-08-29T01:36:51Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-29T13:34:07Z

I like C.... although that means that we need to bump the API version to v1alpha2. That's fine. The API is alpha.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-29T13:47:03Z

Agree, C is better.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-08-29T14:46:58Z

Thanks for your comments. I think so too.
Do we remove the old API (v1alph1)? Or keep it?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-29T14:57:00Z

Remove it. But please add a release note in the CHANGELOG folder (in a new file for 0.3)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-08-29T14:58:41Z

> please add a release note in the CHANGELOG folder

It makes sense.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-08T21:35:46Z

Late question, why do we need to make them configurable, do we really expect admins to change them?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-08T21:52:01Z

It's an extreme case, but some people might need to. For example, to install kueue in their own namespace, instead of asking an admin to install it. Although with cluster-scoped resources, they might still not have the permissions.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-08T21:52:53Z

But more generally, the container shouldn't make assumptions about in which namespace it is running.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-08T21:56:47Z

The namespace is fine to make it configurable, I was mostly referring to the other parameters (service names and such). I am not against it in principle, I just hope we don't clutter the component config API.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-09-09T05:36:29Z

I'm ok with this since we defined these fields in an embedded struct `InternalCertManagement`. If people is really interest with these configurations, he/she can visit this struct. Or just ignore it.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-09T15:59:09Z

General suggestion: I would be more conservative moving forward and expose new configs mostly when there is an explicit ask and a valid use case to keep a lean and simple to configure controller. 

Assuming that admins can just ignore those extra configs is not a good UX, if it is exposed, then we are saying that admins should consider configuring it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-09-09T16:25:07Z

Sorry for that. We haven't release a new version yet, we can still do something. So do you mean configuring them via CLI flags? I mean `ServiceName` and `SecretName `

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-09T16:35:21Z

I wouldn't change anything now, just a general advise on how to look at CC moving forward.
