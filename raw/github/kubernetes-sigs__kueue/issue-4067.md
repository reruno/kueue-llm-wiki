# Issue #4067: Align waitForPodsReady defaults with other fields in config API

**Summary**: Align waitForPodsReady defaults with other fields in config API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4067

**Last updated**: 2025-08-04T08:17:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-01-27T13:10:59Z
- **Updated**: 2025-08-04T08:17:21Z
- **Closed**: 2025-08-04T08:17:21Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to add `waitForPodsReady` to configuration by default, which is now commented out. It shouldn't have any impact though as it's disabled by default.

**Why is this needed**:
This will increase consistency in the [`defaults.go`](https://github.com/kubernetes-sigs/kueue/blob/main/apis/config/v1beta1/defaults.go#L118-L141) file.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-28T21:58:07Z

/help
/good-first-issue

You want to add this as default with WaitForPodsReady disabled?

https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/controller_manager_config.yaml#L26

Just uncomment WaitForPodsReady and disable it?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-28T21:58:09Z

@kannon92: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4067):

>/help
>/good-first-issue
>
>You want to add this as default with WaitForPodsReady disabled?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@OMNARAYANYU](https://github.com/OMNARAYANYU) — 2025-02-10T02:56:46Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-02-10T08:57:56Z

> /help /good-first-issue
> 
> You want to add this as default with WaitForPodsReady disabled?
> 
> https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/controller_manager_config.yaml#L26
> 
> Just uncomment WaitForPodsReady and disable it?

Exactly

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-17T18:50:10Z

IIUC, if `waitForPodsReady` is null, we do not configure it: https://github.com/kubernetes-sigs/kueue/blob/06d4c763ce03891dc0f869e42d5557f9831f1682/apis/config/v1beta1/defaults.go#L119

So, my question is, what is the motivation to configure those parameters by default?

### Comment by [@OMNARAYANYU](https://github.com/OMNARAYANYU) — 2025-02-18T03:32:51Z

> IIUC, if `waitForPodsReady` is null, we do not configure it:
> 
> [kueue/apis/config/v1beta1/defaults.go](https://github.com/kubernetes-sigs/kueue/blob/06d4c763ce03891dc0f869e42d5557f9831f1682/apis/config/v1beta1/defaults.go#L119)
> 
> Line 119 in [06d4c76](/kubernetes-sigs/kueue/commit/06d4c763ce03891dc0f869e42d5557f9831f1682)
> 
>  if cfg.WaitForPodsReady != nil { 
> So, my question is, what is the motivation to configure those parameters by default?

are you recommending this to be an invalid issue?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T07:43:48Z

> > IIUC, if `waitForPodsReady` is null, we do not configure it:
> > [kueue/apis/config/v1beta1/defaults.go](https://github.com/kubernetes-sigs/kueue/blob/06d4c763ce03891dc0f869e42d5557f9831f1682/apis/config/v1beta1/defaults.go#L119)
> > Line 119 in [06d4c76](/kubernetes-sigs/kueue/commit/06d4c763ce03891dc0f869e42d5557f9831f1682)
> > if cfg.WaitForPodsReady != nil {
> > So, my question is, what is the motivation to configure those parameters by default?
> 
> are you recommending this to be an invalid issue?

Sorry for your confusion. I would like to ask this to @PBundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-02-24T13:23:49Z

My primary motivation was to increase consistency across the `defaults.go` file. Than we could also default the values there, and disable it by default. However with the new changes to the `waitForPodsReady` field and taking into the account the discussion [here](https://github.com/kubernetes-sigs/kueue/pull/4302#discussion_r1965344895) I would abandon this idea. Sorry for the late reply

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-02-24T13:24:50Z

Sorry for the confusion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-02-26T15:24:57Z

After some discussions with @mimowo  we came to the conclusion that we wouldn't like to uncomment `waitForPodsReady` field in the Kueue config but rather just stick with cleaning up the `defaults.go` file, so it's consistent with other config fields

### Comment by [@OMNARAYANYU](https://github.com/OMNARAYANYU) — 2025-03-02T03:46:08Z

@PBundyra : Are you suggesting closing this issue w/o making any code fix or are you proposing to make changes in the defaults.go file by adding if condition with null check om waitForPodsReady and then setting all the parameters which we planned to set up in the yaml initially?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-03T08:46:56Z

The latter one, we don't have to close this issue, just make changes to defaults.go

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-30T08:48:17Z

/unassign @OMNARAYANYU

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-30T09:01:35Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-30T09:05:16Z

https://github.com/kubernetes-sigs/kueue/pull/5802

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:58:46Z

@PBundyra can we close this?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T08:17:21Z

Oh yes this was addressed in https://github.com/kubernetes-sigs/kueue/pull/5802
