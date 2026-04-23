# Issue #7245: ☂️ Release 0.15 Plan

**Summary**: ☂️ Release 0.15 Plan

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7245

**Last updated**: 2025-11-24T17:03:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T12:34:51Z
- **Updated**: 2025-11-24T17:03:23Z
- **Closed**: 2025-11-24T17:03:22Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 12

## Description

As usual it is time to compile the list of issues for 0.15. The tentative release date is 17 th November as per https://github.com/kubernetes-sigs/kueue/issues/3588#issuecomment-2615210474

Nice to Haves

- https://github.com/kubernetes-sigs/kueue/issues/7113
- https://github.com/kubernetes-sigs/kueue/issues/6757 
- https://github.com/kubernetes-sigs/kueue/issues/7035
- https://github.com/kubernetes-sigs/kueue/issues/7214
- https://github.com/kubernetes-sigs/kueue/issues/3258
- https://github.com/kubernetes-sigs/kueue/issues/7220
- https://github.com/kubernetes-sigs/kueue/issues/6915
- https://github.com/kubernetes-sigs/kueue/issues/6334
- https://github.com/kubernetes-sigs/kueue/issues/6488
- https://github.com/kubernetes-sigs/kueue/issues/6184
- https://github.com/kubernetes-sigs/kueue/issues/5313
- https://github.com/kubernetes-sigs/kueue/issues/5704
- https://github.com/kubernetes-sigs/kueue/issues/7244
- https://github.com/kubernetes-sigs/kueue/issues/6714
- https://github.com/kubernetes-sigs/kueue/issues/7213
- https://github.com/kubernetes-sigs/kueue/issues/6658
- https://github.com/kubernetes-sigs/kueue/issues/7610

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T12:35:59Z

cc @tenzen-y @gabesaba @kannon92 @amy @mwysokin

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-13T16:25:11Z

LGTM!

### Comment by [@khrm](https://github.com/khrm) — 2025-11-04T09:33:04Z

Can we plan for #2349 to move to beta?  We have tested it, but we expected a thorough testing to be done either this week or before next week.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T09:36:17Z

If no objections I think this is ok, the feature is anyway controlled by configMap knob which provides safety. Yes, some end-to-end testing and adoption will be extra helpful to guide the decision.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-04T12:51:56Z

@khrm wouls you be able to put up a PR to promote that feature to beta?

### Comment by [@khrm](https://github.com/khrm) — 2025-11-04T12:56:45Z

Yes. @kannon92 This week we are doing some multicluster performance benchmarking using this feature. I will raise this next week.

### Comment by [@amy](https://github.com/amy) — 2025-11-04T17:02:36Z

@khrm would be super curious if y'all are allowed to publish the results of the benchmarking

### Comment by [@khrm](https://github.com/khrm) — 2025-11-14T14:54:46Z

@amy Sure. I would share this in next WG call.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T18:40:46Z

As we are approaching the release, let me list the remaining ones based on priority / time to finish

Still trying to get them in:
- https://github.com/kubernetes-sigs/kueue/issues/6757 
- https://github.com/kubernetes-sigs/kueue/issues/6334
- https://github.com/kubernetes-sigs/kueue/issues/6714
- https://github.com/kubernetes-sigs/kueue/issues/5704
- https://github.com/kubernetes-sigs/kueue/issues/7610

Unlikely at this point:
- https://github.com/kubernetes-sigs/kueue/issues/7035
- https://github.com/kubernetes-sigs/kueue/issues/6488
- https://github.com/kubernetes-sigs/kueue/issues/6915

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T11:02:38Z

Adding to consider: https://github.com/kubernetes-sigs/kueue/issues/7610

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T17:03:18Z

/close 
Let's track the remaining discussion under https://github.com/kubernetes-sigs/kueue/issues/7626

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-24T17:03:23Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7245#issuecomment-3571819884):

>/close 
>Let's track the remaining discussion under https://github.com/kubernetes-sigs/kueue/issues/7626


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
