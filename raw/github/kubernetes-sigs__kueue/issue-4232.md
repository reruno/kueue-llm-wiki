# Issue #4232: Support concurrent container image building in cloudbuild

**Summary**: Support concurrent container image building in cloudbuild

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4232

**Last updated**: 2026-01-08T10:37:08Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-11T20:41:21Z
- **Updated**: 2026-01-08T10:37:08Z
- **Closed**: 2026-01-08T10:37:07Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We would like to concurrency perform container image buildings with `make -j 3 image-push debug-image-push importer-image-push helm-chart-push kueue-viz-image-push` in the below script:

https://github.com/kubernetes-sigs/kueue/blob/2738e8b05c03fe5dcf38beba1f4769fe2e1888c9/cloudbuild.yaml#L8-L14

Note: The cloudbuild environment does not support launching multiple QEMU environemnts at the same time as we can check: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/post-kueue-push-images/1889255570226024448

```shell
mount: mounting binfmt_misc on /proc/sys/fs/binfmt_misc failed: Resource busy
mount: mounting binfmt_misc on /proc/sys/fs/binfmt_misc failed: Resource busy
Setting /usr/bin/qemu-alpha-static as binfmt interpreter for alpha
Setting /usr/bin/qemu-alpha-static as binfmt interpreter for alpha
sh: write error: File exists
[...]
```

The possible solution is leveraging the `docker manifests create --amend`. The current building scripts delegates to `docker build --platform=linux/amd64,linux/arm64,linux/ppcle64` to build multi-arch container image at a single image tag.

But I guess that concurrently building should work fine if we can manually merge those images (each platform images) the similar to [cluter-api repository](https://github.com/kubernetes-sigs/cluster-api/blob/main/Makefile) in the following:

1. Build each image separately with `docker buildx build --platform=[linux/amd64|linux/arm64|linux/ppcle64]`
2. Merge container image manifests with `docker manifest create --amend XXX`

**Why is this needed**:
Even though we increase machine size, the post commits container image buildings significantly slower as we can see: https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/logs/post-kueue-push-images?buildId=

Once we can perform those concurrently, we can easily and faster provide staging and production images.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.
- concurrency building investigation in cluster-api repository: https://github.com/kubernetes-sigs/kueue/pull/4222#issuecomment-2650505614
- machine size change (`N1_HIGHCPU_8 ` -> `E2_HIGHCPU_32`) affection: https://github.com/kubernetes-sigs/kueue/pull/4222#issuecomment-2651473165

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-11T20:41:33Z

cc: @mimowo

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-12T21:13:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-13T04:31:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-11T05:03:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T08:43:47Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-09T09:19:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-09T10:06:34Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-08T10:37:02Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-08T10:37:08Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4232#issuecomment-3723249242):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
